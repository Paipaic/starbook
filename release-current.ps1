param(
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Join-Path $Root $Path), $Content, $encoding)
}

function Write-PowerShellUtf8 {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )
    # Windows PowerShell 5.1 needs a BOM to reliably read non-ASCII script text.
    $encoding = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText((Join-Path $Root $Path), $Content, $encoding)
}

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found."
    }
}

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

Require-Command git
Require-Command python
Require-Command node
Require-Command gh

Run-Step "Check Git repository" { git rev-parse --is-inside-work-tree | Out-Null }

if (-not (Test-Path "VERSION")) {
    throw "VERSION is missing. Set the target version first (example: 1.6.1)."
}

$PlainVersion = (Get-Content -LiteralPath "VERSION" -Raw -Encoding UTF8).Trim()
if ($PlainVersion.StartsWith("v")) {
    $PlainVersion = $PlainVersion.Substring(1)
}
if ($PlainVersion -notmatch '^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$') {
    throw "VERSION '$PlainVersion' is not a supported semantic version. Example: 1.6.1"
}

$TagVersion = "v$PlainVersion"
$Branch = "release/$TagVersion"
$LegacyBranch = "release/$PlainVersion"

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "Starbook $TagVersion release"
}

$currentBranch = (git branch --show-current).Trim()
if (-not $currentBranch) {
    throw "Detached HEAD is not supported. Checkout main or a release branch first."
}

# Normalize the common typo: release/1.6.0 -> release/v1.6.0
if ($currentBranch -eq $LegacyBranch) {
    Write-Host "Normalizing branch '$LegacyBranch' -> '$Branch'" -ForegroundColor Yellow
    Run-Step "Rename release branch" { git branch -m $Branch }
    $currentBranch = $Branch
}

if ($currentBranch -ne "main" -and $currentBranch -ne $Branch) {
    throw "Current branch is '$currentBranch'. VERSION=$PlainVersion expects main or '$Branch'."
}

# If work was done directly on main, only continue when local main still matches origin/main.
# This avoids another automatic stash/rebase conflict. publish.ps1 will create the release branch.
if ($currentBranch -eq "main") {
    Run-Step "Fetch latest main" { git fetch origin main }
    $localMain = (git rev-parse main).Trim()
    $remoteMain = (git rev-parse origin/main).Trim()
    if ($localMain -ne $remoteMain) {
        throw "Local main is not aligned with origin/main. Preserve your work, update main, then rerun release-current.ps1. Automatic stash/rebase is intentionally disabled to avoid conflict loss."
    }
}

$statusLines = @(git status --short)
$releaseDir = Join-Path $Root "docs\releases"
$scriptDir = Join-Path $Root "scripts\releases"
New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
New-Item -ItemType Directory -Force -Path $scriptDir | Out-Null

# Keep obvious current-version declarations synchronized.
if (Test-Path "blocks\00-config.html") {
    $cfg = Get-Content -LiteralPath "blocks\00-config.html" -Raw -Encoding UTF8
    $cfg = $cfg -replace "version:\s*'[^']+'", "version: '$PlainVersion'"
    Write-Utf8NoBom "blocks\00-config.html" $cfg
}
if (Test-Path "PROJECT_STATE.md") {
    $state = Get-Content -LiteralPath "PROJECT_STATE.md" -Raw -Encoding UTF8
    $state = $state -replace '(?m)^- Version: `[^`]+`', "- Version: ``$PlainVersion``"
    $state = $state -replace '(?m)^- Runtime config version: `[^`]+`\.', "- Runtime config version: ``$PlainVersion``."
    Write-Utf8NoBom "PROJECT_STATE.md" $state
}
if (Test-Path "AGENTS.md") {
    $agents = Get-Content -LiteralPath "AGENTS.md" -Raw -Encoding UTF8
    $agents = $agents -replace '(?m)^- Current version: \*\*[^*]+\*\*', "- Current version: **$PlainVersion**"
    Write-Utf8NoBom "AGENTS.md" $agents
}
if (Test-Path "README.md") {
    $readme = Get-Content -LiteralPath "README.md" -Raw -Encoding UTF8
    $readme = $readme -replace '当前正式项目版本：\*\*v[^*]+\*\*。', "当前正式项目版本：**$TagVersion**。"
    Write-Utf8NoBom "README.md" $readme
}

# Create a release record only when the version does not already have one.
$releaseRecordRel = "docs\releases\$TagVersion.md"
$releaseRecord = Join-Path $Root $releaseRecordRel
if (-not (Test-Path $releaseRecord)) {
    $date = Get-Date -Format "yyyy-MM-dd"
    $changedText = if ($statusLines.Count -gt 0) { ($statusLines | ForEach-Object { "- ``$_``" }) -join "`n" } else { "- 运行脚本时未检测到未提交文件；以最终 PR diff 为准。" }
    $hasSupabaseChanges = ($statusLines -join "`n") -match 'supabase[\\/]'
    $dataNote = if ($hasSupabaseChanges) {
        "检测到 ``supabase/`` 目录变化。代码发布不会自动执行 SQL；必须在 Production 操作前人工核对 migration / seed 的影响。"
    } else {
        "发布自动化不会重置 Supabase。未检测到未提交的 ``supabase/`` 文件变化；如实际存在数据变更，以 migration 与 PR diff 为准。"
    }

    $record = @"
# Starbook $TagVersion

> 本 Release Record 由 ``release-current.ps1`` 在 $date 自动建立。Agent/开发者应在版本迭代过程中补充具体产品与架构变化；自动生成只保证发布治理链路完整，不替代人工设计记录。

## 1. 版本目标

$Message

## 2. 用户可见变化

- 以本版本实际实现和最终 PR diff 为准；如已有明确功能说明，请在发布前补充到此处。

## 3. Runtime 链路变化

- 默认沿用上一版本 Runtime 链路；若本版修改 ``SB.user / SB.book / SB.magicBook / SB.theme / SB.experience / SB.store``，必须在此明确记录。

## 4. 架构 / 扩展契约变化

- 默认不改变长期扩展契约；任何多用户、多 Book、Relationship、Theme、Experience 边界变化必须明确记录。

## 5. Auth / Membership / RLS 变化

- 默认无变化；如有变化，以本版 migration / RLS 与 PR diff 为准。

## 6. 数据模型 / Migration 变化

$dataNote

## 7. Storage / Media 变化

- 默认沿用 Private Storage ``starbook-media``；如有路径、权限或媒体格式变化必须补充。

## 8. Git / Branch / PR / Merge 链路变化

- ``$Branch → PR → validate-starbook → squash merge → main → GitHub Pages``。
- 使用 ``release-current.ps1`` 作为版本完成后的首选一键发布入口。

## 9. CI / Validation 变化

- 一键发布会执行 ``python build.py``、``python tools/check_project.py``、Secret marker 扫描，再由 PR 的 ``validate-starbook`` 复检。

## 10. GitHub Pages / Production Deploy 变化

- ``main`` 仍是唯一 Production branch；普通代码发布不重置 Supabase 数据。

## 11. Agent / 文档治理变化

- 当前版本的发布记录与版本专属发布脚本可由 ``release-current.ps1`` 自动生成。
- Agent 仍需根据真实改动维护 CHANGELOG / ROADMAP / PROJECT_STATE 与架构文档。

## 12. 新增文件

- 自动生成：``scripts/releases/release-$TagVersion.ps1``。
- 本文件：``$releaseRecordRel``。

## 13. 修改文件

$changedText

## 14. 删除文件

- 以最终 PR diff 为准。

## 15. 用户需要手动操作

常规代码版本只需在项目根目录运行：

~~~powershell
.\release-current.ps1
~~~

如需自定义 PR / commit 描述：

~~~powershell
.\release-current.ps1 -Message "本版主要改动"
~~~

若本版包含 Supabase migration，SQL 仍需按 migration 文档人工执行；脚本不会自动修改 Production Database。

## 16. 测试与验证

- 本地 build / check_project 由发布脚本自动执行。
- PR 上 ``validate-starbook`` 必须通过。
- 发布后仍需完成 Production smoke test。

## 17. Production 数据影响

- 是否需要重新导入旧数据？默认否。
- 是否需要运行 SQL？仅当本版存在明确 migration 时需要。
- 是否会删除/覆盖现有数据？发布脚本本身不会。

## 18. 已知问题

- 以本版测试结果补充。

## 19. 回滚方案

- 前端回滚：revert 对应 release merge commit，由 ``main`` 重新部署 Pages。
- 数据回滚不得通过 reset Supabase 实现；有 migration 时必须使用对应的 forward-fix / 明确回滚方案。

## 20. 待优化项

- 以 ROADMAP 与本版测试结果补充。

## 21. 下一版本建议

- 以 ROADMAP 为准。
"@
    Write-Utf8NoBom $releaseRecordRel $record
    Write-Host "Created release record: $releaseRecordRel" -ForegroundColor Green
} else {
    Write-Host "Release record already exists; preserving it: $releaseRecordRel" -ForegroundColor DarkGray
}

# Ensure CHANGELOG has a current-version section. Existing content is never overwritten.
if (Test-Path "CHANGELOG.md") {
    $changelog = Get-Content -LiteralPath "CHANGELOG.md" -Raw -Encoding UTF8
    $versionPattern = [regex]::Escape("[$PlainVersion]")
    if ($changelog -notmatch $versionPattern) {
        $date = Get-Date -Format "yyyy-MM-dd"
        $entry = @"
## [$PlainVersion] - $date

### Release
- $Message

### CI / Governance
- 版本发布使用 ``release-current.ps1``：从 ``VERSION`` 自动解析版本、生成缺失的 Release Record 与版本专属发布脚本，再进入既有 PR / CI / Pages 链路。

### Data
- 发布自动化不会重置 Supabase；如本版存在 migration，仍按 Release Record 人工执行 Production SQL。

"@
        if ($changelog.StartsWith("# Changelog")) {
            $rest = $changelog.Substring("# Changelog".Length).TrimStart([char[]]"`r`n")
            $changelog = "# Changelog`n`n$entry$rest"
        } else {
            $changelog = "$entry$changelog"
        }
        Write-Utf8NoBom "CHANGELOG.md" $changelog
        Write-Host "Added CHANGELOG section for $PlainVersion" -ForegroundColor Green
    }
}

# Generate a version-specific wrapper script for auditability/repeatability.
$versionScriptRel = "scripts\releases\release-$TagVersion.ps1"
$escapedMessage = $Message.Replace('`', '``').Replace('"', '`"')
$versionScript = @"
param(
    [string]`$Message = "$escapedMessage"
)

`$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
`$Root = (Resolve-Path (Join-Path `$PSScriptRoot "..\..")).Path
Set-Location `$Root

Write-Host "Publishing Starbook $TagVersion" -ForegroundColor Cyan
& (Join-Path `$Root "publish.ps1") -Version "$PlainVersion" -Message `$Message
"@
Write-PowerShellUtf8 $versionScriptRel $versionScript
Write-Host "Generated version release script: $versionScriptRel" -ForegroundColor Green

# Use the generated version-specific script so the exact release command is committed with the version.
Write-Host "`nStarbook $TagVersion release is prepared." -ForegroundColor Green
Write-Host "Target branch: $Branch" -ForegroundColor Green
Write-Host "Release record: $releaseRecordRel" -ForegroundColor Green
Write-Host "Version script: $versionScriptRel" -ForegroundColor Green

& (Join-Path $Root $versionScriptRel) -Message $Message
