# Starbook Release Workflow

> 本文负责“怎么发版本”。项目整体治理原则见 `PROJECT_MANAGEMENT_FULL_CHAIN.md`。

## 1. Production rule

`main` 是唯一 Production branch。

```text
release/vX.X.X or feature/*
        ↓
Pull Request
        ↓
validate-starbook
        ↓
merge main
        ↓
Deploy Starbook to GitHub Pages
```

GitHub Pages 的公网 URL 始终不因 release branch 名称变化而改变。

Supabase Database / Private Storage 与 Git 分支独立。普通前端发布不会重置真实 Book 数据。

## 2. GitHub 一次性设置

- `deploy-pages.yml` 只监听 `main`；
- `validate.yml` 在 PR → main 时运行；
- Settings → General → Pull Requests：允许 Auto-merge（可选但推荐）；
- `main` protection/ruleset：
  - Require pull request；
  - Require `validate-starbook`；
  - 禁止 force push；
  - 禁止删除 main；
- `github-pages` Environment 只允许 `main` 部署。

## 3. 本地一次性设置

需要：

```text
Git
Python
Node.js
gh (GitHub CLI)
```

GitHub CLI：

```powershell
winget install --id GitHub.cli --source winget
gh auth login
gh auth status
```

## 4. 每个版本发布前的文档要求

以 `1.5.2` 为例，发布前必须存在/更新：

```text
VERSION                         → 1.5.2
CHANGELOG.md                    → [1.5.2]
PROJECT_STATE.md                → Current Release = 1.5.2
ROADMAP.md                      → 状态同步
docs/releases/v1.5.2.md        → 完整 release record
```

如果管理、架构、数据或部署规则发生变化，还要同步：

```text
AGENTS.md
docs/PROJECT_MANAGEMENT_FULL_CHAIN.md
docs/ARCHITECTURE_EXTENSION_CONTRACT.md
docs/DATA_LIFECYCLE.md
docs/RELEASE_WORKFLOW.md
```

## 5. Release Record 必写内容

模板：

```text
docs/templates/RELEASE_RECORD_TEMPLATE.md
```

每版必须说明：

- 用户体验；
- Runtime；
- 架构扩展契约；
- Auth / Membership / RLS；
- Data / Migration；
- Storage；
- Git / PR / Merge；
- CI；
- Pages；
- Agent / 文档治理；
- 手动操作；
- Production 数据影响；
- 回滚。

某项没有变化也要明确写“无变化”。

## 6. 本地发布

完成版本代码和文档后运行：

```powershell
.\publish.ps1 -Version 1.5.2 -Message "版本说明"
```

脚本会：

1. 确认 Git / Python / Node / gh；
2. 从最新 `main` 创建/使用 `release/v1.5.2`；
3. 对齐 `VERSION`；
4. 检查 release record / changelog / project state；
5. 执行 `python build.py`；
6. 执行 `python tools/check_project.py`；
7. 扫描高风险 Secret marker；
8. commit + push；
9. 创建 PR；
10. 请求 Auto-merge；
11. GitHub 等待 required checks；
12. merge main 后 Pages 自动部署。

## 7. 数据规则

普通版本发布：

- 不重新运行 `002_anniversary_owner.sql`；
- 不清空 `book_data`；
- 不删除 Storage；
- 不要求重新导入数据。

需要 schema 变化时：

- 新增 migration 文件；
- 迁移旧数据向前；
- release record 明确说明；
- production SQL 由用户按步骤执行；
- 不把 reset 当 migration。

## 8. 发布后的 Production smoke test

至少验证：

- Production URL 打开；
- Auth；
- Book 加载；
- 主要 Scene；
- 本版本核心功能；
- 已有城市/回忆仍存在；
- Private 图片/BGM 仍可读取。

## 9. Tag

重要正式版本发布完成后建议：

```powershell
git checkout main
git pull --ff-only origin main
git tag v1.5.2
git push origin v1.5.2
```

周年最终交付版必须打 tag。
