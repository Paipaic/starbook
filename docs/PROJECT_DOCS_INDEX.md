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
9. `PERFORMANCE_GUIDE.md` —— v1.7.2 起的场景、图片、Canvas 与响应式性能基线。

## 视觉设计（Magic Celestial Theme）

- `design/VISUAL_UPGRADE_PLAN.md` — v1.5.2 → v1.7.x 视觉升级总计划、乱码根因实测、奇幻电影与电影式剪辑调研及来源。
- `../prompts/00-typography.md` — 「星文」字体系统提示词（v1.5.2）。
- `../prompts/11-memory-player.md` — 「光影放映」多图编排放映、三种放映风格与四季主题提示词（v1.7.0，取代 v1.6.0 版本；v1.9.1 第 12–13 节分组放映与自动 / 手动；v1.9.2 第 14–15 节镜头语言库与电影模式）。
- `../prompts/12-memory-editor.md` — 回忆编辑器「星屿手稿」提示词（v1.7.0；v1.9.0 影像管理台；v1.9.1 照片分组「同一时刻」）。
- `../prompts/10-city-album.md` — 城市回忆目录页「星屿手稿 · 目录页」提示词（v1.7.1）。
- `../prompts/00-gate.md` — 「秘境之门」转场提示词（v1.8.1 重写：五种门按路线区分、曝光规则、放慢光线）。
- `../prompts/02-menu.md` — 菜单（只保留世界星图 / 时光长卷）与右上角工具标识 `SB.dock`（v1.8.1；v1.8.2 增加「回到魔法书」）。
- `../prompts/04-book-opening.md` — 开书特效「星尘启封」（v1.8.2 重写；v1.8.3 机关启封）。
- `../prompts/00-login-gate.md` — 登录 / 启动门「星盘启封」（v1.9.0）。
- `../tools/make_admin.py` — 生成中国 / 美国行政区划搜索库 `blocks/06-admin-divisions.html`（v1.9.0）。
- `../prompts/13-overview.md` — 「时光长卷」横向时间轴（v1.8.1，取代回忆总览；v1.10.0「时光之环」三维环形时光轴 + 周年节点）。
- `../prompts/14-year-reel.md` — 「时光剪影」周年回放（v1.10.0）。
- `../prompts/03-magic-book.md`、`../prompts/07-globe.md` — 「星辉层次」魔法书与地球特效、地球搜索栏（v1.8.0）。
- `../prompts/09-country-map.md` — 国家地图；v1.8.0 起返回直接回到地球（大洲目录页已删除）。
- `../tools/make_cities.py` — 生成离线城市库 `blocks/06-world-cities.html`（v1.8.0）。

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

## 场景性能逐链路 Prompt（v1.7.3）

- `prompts/performance/01-login-to-book.md`
- `prompts/performance/02-book-to-globe.md`
- `prompts/performance/03-globe-to-country.md`
- `prompts/performance/04-country-city-deep-scenes.md`
- `prompts/performance/05-scene-runtime-transaction.md`

## v1.7.3 转场专项验收

- `docs/TRANSITION_STABILITY_TEST.md`：登录→Book→Globe→Country→City→Player 全链路真机验收（v1.8.0 增加秘境之门与搜索验收项）。
