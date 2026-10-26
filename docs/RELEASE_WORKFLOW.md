# Starbook Release Workflow

## Production rule

`main` is the only production branch. GitHub Pages deploys only from `main`.

Supabase Database and Private Storage are independent from Git branches. A normal frontend release does not reset existing Book data, memories, photos, or music.

## One-time GitHub setup

1. Keep `.github/workflows/deploy-pages.yml` listening only to `main`.
2. Add `.github/workflows/validate.yml` to `main`.
3. In **Settings → General → Pull Requests**, enable **Allow auto-merge**.
4. Protect `main` using a branch protection rule or ruleset:
   - Require a pull request before merging.
   - Require status checks to pass before merging.
   - Require check: `validate-starbook`.
   - Do not allow force pushes.
   - Do not allow branch deletion.
5. In **Settings → Environments → github-pages**, allow only `main` to deploy.

## One-time local setup

Install GitHub CLI on Windows:

```powershell
winget install --id GitHub.cli --source winget
```

Close the terminal/VS Code window completely, reopen it, then:

```powershell
gh auth login
```

Choose GitHub.com → HTTPS → Login with a web browser.

Verify:

```powershell
gh auth status
```

## Publishing a new version

After making the desired changes locally, run from the repository root:

```powershell
.\publish.ps1 -Version 1.5.1 -Message "手机端返回与交互优化"
```

The script will:

1. Create/use `release/v1.5.1`.
2. Update `VERSION`.
3. Run `python build.py`.
4. Run `python tools/check_project.py`.
5. Scan the built site for high-risk secret markers.
6. Commit and push the release branch.
7. Create a PR into `main`.
8. Enable GitHub Auto-merge.
9. Wait on GitHub for `validate-starbook` to pass.
10. GitHub merges to `main` automatically.
11. The existing Pages workflow deploys `main` automatically.

The public URL does not change.

## Data rule

Normal code releases must never re-run destructive seed/reset SQL against production data.

Database schema changes must use additive/migrating SQL files. Existing Book data must be migrated forward rather than deleted and re-imported.
