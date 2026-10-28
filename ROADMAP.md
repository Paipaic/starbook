
## v1.8.3 — 开书「机关启封」

- [x] 机关逐级啮合 + 棘轮步进、宝石旋转、能量描线与光珠、星辰依次点亮、机关火花、解锁

## v1.8.2 — 真机反馈：回到魔法书 · 星尘启封 · 手机性能

- [x] 右上角「回到魔法书」标识
- [x] 开书特效重做（扉页金墨星图 + 星尘，无汇聚 / 闪白）
- [x] 手机：开书不再冻结、去除光球与闪烁、启动提速

## v1.8.1 — 柔光 · 分路转场 · 星夜摩洛哥皮 · 时光长卷

- [x] 去除开书汇聚与门钥匙的过曝
- [x] 五种门按路线区分，光线放慢
- [x] 魔法书材质、颜色、渲染重新设计
- [x] 菜单只保留世界星图 / 时光长卷；右上角音乐 / 动效 / 账户标识
- [x] 「时光长卷」可拖动时间轴
- [x] 城市空状态重排

## v1.8.0 — 秘境之门 · 星辉层次 · 搜索与导航

- [x] 「秘境之门」门钥匙 / 幻影显形 / 熄灯器三种转场（`SB.gate`，可回退）
- [x] 「星辉层次」魔法书与地球特效
- [x] 删除大洲国家目录页，国家返回直接回到地球
- [x] 地球搜索栏（我们的城市 / 国家 / 任意城市，离线 + 在线）

## v1.7.3 — Scene Transaction / First-frame Stability

- [x] 登录 Gate 延迟到 Book 首帧后揭开
- [x] Scene Manager await prepare / enter / nextPaint
- [x] Globe / Country / City / Player 首屏资源预取
- [x] Portal backdrop 防旧页残留
- [x] 逐链路性能 Prompt 固化

# Starbook Roadmap

## Visual Upgrade — Magic Celestial Theme（计划见 `docs/design/VISUAL_UPGRADE_PLAN.md`）

- **VIS-001 · 「星文」字体系统 / 乱码修复** — `DONE` (v1.5.2)
- **VIS-004 · 「冥想盆放映厅」电影式回忆放映 + 放映按钮** — `DONE` (v1.6.0)
- **VIS-005 · 「光影放映」多图编排放映 + 三种放映风格（银幕 / 星图 / 手札）** — `DONE` (v1.7.0)
- **VIS-006 · 放映四季主题（春 / 夏 / 秋 / 冬调色与粒子）** — `DONE` (v1.7.0)
- **VIS-007 · 回忆编辑器「星屿手稿」界面升级（实时海报预览、照片卡片、风格 / 季节选择）** — `DONE` (v1.7.0)
- **VIS-008 · 城市回忆目录页「星屿手稿 · 目录页」升级** — `DONE` (v1.7.1)
- **PERF-001 · 场景切换 / 移动端 / 放映图片 / 深层页面比例性能优化** — `DONE` (v1.7.2)
- **VIS-002 · 「秘境之门」奇幻转场系统** — `DONE` (v1.8.0)
- **VIS-003 · 「星辉层次」魔法书与地球特效** — `DONE` (v1.8.0)
- **NAV-001 · 导航精简（删除大洲目录页）+ 地球城市 / 国家搜索栏** — `DONE` (v1.8.0)
- **VIS-009 · 转场柔光与分路（门钥匙 / 幻影显形 / 墨金书页 / 冥想盆 / 熄灯器）** — `DONE` (v1.8.1)
- **VIS-010 · 魔法书「星夜摩洛哥皮」材质重设计** — `DONE` (v1.8.1)
- **NAV-002 · 菜单精简 + 右上角工具标识 `SB.dock`** — `DONE` (v1.8.1)
- **TL-001 · 「时光长卷」时间轴（取代回忆总览）** — `DONE` (v1.8.1)
- **PERF-002 · 手机魔法书性能与渲染稳定（开书冻结 / 光球 / 闪烁 / 启动）** — `DONE` (v1.8.2)
- **VIS-011 · 开书特效「星尘启封」** — `DONE` (v1.8.2)
- **VIS-012 · 开书第一阶段「机关启封」** — `DONE` (v1.8.3)
- v1.7.2 改为性能与响应式优化版本；VIS-002 / VIS-003 按 Owner 要求在 v1.8.0 完成，并保持 v1.7.3 场景事务与性能分档。
- 后续可选：放映风格增加第 4 种；编辑器内「预览放映」按钮；照片焦点（兴趣点）标记（需新增字段）。

## Project Governance — v1.5.1

- **GOV-001 · Agent Handoff** — `DONE` — 根目录 `AGENTS.md` + 必读顺序。
- **GOV-002 · Full-chain documentation** — `DONE` — 项目开发、CI/CD、数据、回滚、交接链路固化。
- **GOV-003 · Release record enforcement** — `DONE` — 每个版本强制记录多维链路变化。
- **GOV-004 · Documentation-aware validation** — `DONE` — 本地 checker + PR CI 校验版本治理文件一致性。
- **GOV-005 · Production branch rule** — `DONE` — `main` 为唯一 Production branch，Pages 只由 main 部署。

## Anniversary P0 — 2026-10-29 前

- **ANN-010 · Runtime / MagicBook 命名冲突** — `DONE` — `SB.book` 保留给数据 Book Context，视觉魔法书改为 `SB.magicBook`。
- **ANN-001 · Supabase 实际初始化** — `DONE` — migration + owner seed + Private Bucket + Auth/RLS 前端访问链路已验证。
- **ANN-002 · Private Storage 实机验证** — `TODO` — 上传照片、刷新、重新签名 URL、删除。
- **ANN-003 · 手机端稳定性** — `DONE` — 100dvh / safe-area / coarse pointer / 误触阈值已加固并完成当前实机验证。
- **ANN-004 · 浏览器/Android 返回测试** — `DONE` — 连续 popstate pending queue 与 bfcache 恢复保护已完成当前实机验证。
- **ANN-005 · 核心 CDN 可靠性** — `IN_PROGRESS` — 动态脚本增加超时 fallback，Three.js 三 CDN；本地 vendor 化不再阻塞周年交付。
- **ANN-006 · 统一错误恢复细化** — `IN_PROGRESS` — 登录/无权限错误已加入可恢复路径与返回登录；业务操作错误状态继续检查。
- **ANN-007 · 周年内容填充** — `TODO` — 城市、回忆、照片、BGM、文案。
- **ANN-008 · 周年献词/结尾** — `PLANNED` — 核心稳定后再实现，不阻塞交付。
- **ANN-009 · Feature Freeze** — `TODO` — 2026-10-28 晚停止新增功能。

## Post-Anniversary P1

- `TODO` V1 JSONB → memories / locations / assets / settings 正规化。
- `TODO` Memory First Architecture；Memory 不再强制依赖 City。
- `TODO` 图片 thumbnail / preview / full 多尺寸资源。
- `TODO` 完整 Router 与可分享深层 URL。
- `TODO` Supabase Realtime。
- `TODO` 数据导出、备份、恢复。
- `TODO` PWA / Service Worker（在更新策略明确后再做）。

## Platform P2

- `TODO` Book Library，多 Book 创建/切换。
- `TODO` 公众注册、邮箱验证、忘记密码、账户管理。
- `TODO` Relationship Type 系统：romantic / family / friendship / personal / travel / custom。
- `TODO` Theme Engine：Magic Celestial 只是第一套 Theme。
- `TODO` Experience System：World Map 只是第一套 Experience。
- `TODO` Timeline / Family Tree / Album / Constellation 等 Experience。
- `TODO` 搜索、标签、收藏、那年今日、年度总结。
