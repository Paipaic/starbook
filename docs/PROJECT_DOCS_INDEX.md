# Starbook Documentation Index

## 新 Agent / 新会话

0. `../README.md` —— 仓库入口；Agent 仍以 `AGENTS.md` 为强制上下文入口。
1. `../AGENTS.md`
2. `../PROJECT_STATE.md`
3. `PROJECT_MANAGEMENT_FULL_CHAIN.md`
4. `ARCHITECTURE_EXTENSION_CONTRACT.md`
5. `DATA_LIFECYCLE.md`
6. `../CHANGELOG.md`
7. `../ROADMAP.md`
8. 当前 `releases/vX.X.X.md`

## 视觉设计（Magic Celestial Theme）

- `design/VISUAL_UPGRADE_PLAN.md` — v1.5.2 → v1.6.2 视觉升级总计划、乱码根因实测、奇幻电影与电影式剪辑调研及来源。
- `../prompts/00-typography.md` — 「星文」字体系统提示词（v1.5.2）。
- `../prompts/11-memory-player.md` — 「光影放映」多图编排放映、三种放映风格与四季主题提示词（v1.7.0，取代 v1.6.0 版本）。
- `../prompts/12-memory-editor.md` — 回忆编辑器「星屿手稿」提示词（v1.7.0）。
- `../prompts/10-city-album.md` — 城市回忆目录页「星屿手稿 · 目录页」提示词（v1.7.1）。

## 发布与 CI

- `V151_OPERATOR_STEPS.md` — v1.5.1 本次发布的 Owner 手动操作清单。
- `RELEASE_WORKFLOW.md`
- `templates/RELEASE_RECORD_TEMPLATE.md`
- `.github/workflows/validate.yml`
- `.github/workflows/deploy-pages.yml`
- `publish.ps1`

## Anniversary Bridge / Supabase

- `ANNIVERSARY_IMPLEMENTATION_BASELINE.md`
- `SUPABASE_ANNIVERSARY_SETUP.md`
- `../supabase/migrations/`（当前 v1.5.1 需要 `002_v151_title_and_members.sql`）
- `../supabase/seed/`

## 测试记录

- `PHASE2_LIVE_TEST.md`
- `PHASE3_STABILITY_TEST.md`

## 文档职责速查

| 文件 | 回答的问题 |
|---|---|
| `AGENTS.md` | 新 Agent 第一眼该做什么？ |
| `PROJECT_STATE.md` | 现在真实状态是什么？ |
| `PROJECT_MANAGEMENT_FULL_CHAIN.md` | 项目从开发到生产如何运转？ |
| `ARCHITECTURE_EXTENSION_CONTRACT.md` | 哪些架构边界不能破坏？ |
| `DATA_LIFECYCLE.md` | 数据为什么不会随版本丢失？如何迁移？ |
| `CHANGELOG.md` | 已经做了什么？ |
| `ROADMAP.md` | 还没做什么？ |
| `releases/vX.X.X.md` | 某个版本到底改变了哪些链路？ |

### `docs/RELEASE_AUTOMATION.md`

v1.6.0+ 一键版本发布机制。说明 `release-current.ps1`、自动 Release Record、版本专属脚本、数据安全边界和失败处理。
