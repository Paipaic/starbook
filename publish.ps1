param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [Parameter(Mandatory = $true)]
    [string]$Message
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Run-Step {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][scriptblock]$Command
    )
    Write-Host "`n==> $Label" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found."
    }
}

Require-Command git
Require-Command python
Require-Command node
Require-Command gh

# Normalize version: 1.5.1 -> v1.5.1
if ($Version.StartsWith("v")) {
    $TagVersion = $Version
} else {
    $TagVersion = "v$Version"
}
$PlainVersion = $TagVersion.Substring(1)
$Branch = "release/$TagVersion"

# Make sure this is a Git repository.
Run-Step "Check Git repository" { git rev-parse --is-inside-work-tree | Out-Null }

# Verify GitHub CLI authentication once. If this fails, run: gh auth login
Run-Step "Check GitHub CLI authentication" { gh auth status | Out-Null }

$currentBranch = (git branch --show-current).Trim()
if (-not $currentBranch) {
    throw "Detached HEAD is not supported. Checkout main or a release branch first."
}

# If publishing from main, ensure main is current before branching.
if ($currentBranch -eq "main") {
    $dirty = git status --porcelain
    Run-Step "Fetch latest main" { git fetch origin main }

    $localMain = (git rev-parse main).Trim()
    $remoteMain = (git rev-parse origin/main).Trim()

    if ($localMain -ne $remoteMain) {
        if ($dirty) {
            throw "Local main is behind origin/main and has uncommitted changes. Commit/stash them first, then rerun."
        }
        Run-Step "Fast-forward main" { git pull --ff-only origin main }
    }

    Run-Step "Create release branch $Branch" { git checkout -b $Branch }
    $currentBranch = $Branch
}
elseif ($currentBranch -ne $Branch) {
    throw "Current branch is '$currentBranch'. For version $TagVersion, use main or '$Branch'."
}

# Keep VERSION aligned with the release branch.
if (Test-Path "VERSION") {
    Set-Content -Path "VERSION" -Value $PlainVersion -Encoding utf8
}

Run-Step "Build Starbook" { python build.py }

if (Test-Path "tools/check_project.py") {
    Run-Step "Run Starbook checks" { python tools/check_project.py }
} else {
    throw "tools/check_project.py is missing. Refusing to publish without validation."
}

# Fail fast if a high-risk credential marker was accidentally built into site/.
# Only inspect deployable text assets. Empty files (for example site/.nojekyll)
# can make Get-Content -Raw return $null in Windows PowerShell, so guard them.
$secretPatterns = @("sb_secret_", "github_pat_", "ghp_")
$textExtensions = @(".html", ".htm", ".js", ".mjs", ".css", ".json", ".txt", ".xml", ".svg", ".webmanifest", ".md")
$secretHits = @()
Get-ChildItem -Path "site" -File -Recurse -ErrorAction Stop | ForEach-Object {
    $file = $_
    $extension = $file.Extension.ToLowerInvariant()
    if ($textExtensions -notcontains $extension) {
        return
    }

    $path = $file.FullName
    try {
        $text = Get-Content -LiteralPath $path -Raw -ErrorAction Stop
    } catch {
        return
    }

    if ([string]::IsNullOrEmpty($text)) {
        return
    }

    foreach ($pattern in $secretPatterns) {
        if ($text.Contains($pattern)) {
            $secretHits += "$path contains $pattern"
        }
    }
}
if ($secretHits.Count -gt 0) {
    $secretHits | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    throw "High-risk secret marker detected in site/. Publish aborted."
}

Run-Step "Stage changes" { git add -A }

$staged = git diff --cached --name-only
if ($staged) {
    Run-Step "Commit $TagVersion" { git commit -m "release: $TagVersion - $Message" }
} else {
    Write-Host "No new local changes to commit; continuing with existing branch commits." -ForegroundColor Yellow
}

Run-Step "Push $Branch" { git push -u origin $Branch }

# Create a PR if the current release branch does not already have one.
$prUrl = (gh pr list --head $Branch --base main --state open --json url --jq '.[0].url').Trim()
if (-not $prUrl) {
    $body = @"
## Starbook $TagVersion

$Message

### Release pipeline
- Local build completed
- Local project checks completed
- GitHub `validate-starbook` must pass before merge
- After merge, `main` deploys automatically to GitHub Pages
- Supabase data is not reset by this release
"@

    Run-Step "Create pull request" {
        gh pr create --base main --head $Branch --title "Starbook $TagVersion - $Message" --body $body
    }
    $prUrl = (gh pr list --head $Branch --base main --state open --json url --jq '.[0].url').Trim()
}

if (-not $prUrl) {
    throw "Could not determine the pull request URL."
}

Write-Host "`nPull request: $prUrl" -ForegroundColor Green

# Enable auto-merge. GitHub will wait for required branch rules/status checks.
Run-Step "Enable auto-merge" {
    gh pr merge $prUrl --auto --squash --delete-branch
}

Write-Host "`nRelease submitted successfully." -ForegroundColor Green
Write-Host "GitHub will merge it into main after required checks pass, then main will deploy Pages automatically." -ForegroundColor Green
Write-Host "Production URL remains unchanged." -ForegroundColor Green
