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
