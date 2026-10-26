# Starbook Roadmap

## Anniversary P0 — 2026-10-29 前

- **ANN-010 · Runtime / MagicBook 命名冲突** — `DONE` — `SB.book` 保留给数据 Book Context，视觉魔法书改为 `SB.magicBook`。
- **ANN-001 · Supabase 实际初始化** — `IN_PROGRESS` — migration + owner seed + Private Bucket 已验证；待真实前端登录完成 RLS 端到端验证。
- **ANN-002 · Private Storage 实机验证** — `TODO` — 上传照片、刷新、重新签名 URL、删除。
- **ANN-003 · 手机端稳定性** — `IN_PROGRESS` — 100dvh / safe-area / coarse pointer / 误触阈值已加固；待真实 iPhone/Android 验证。
- **ANN-004 · 浏览器/Android 返回测试** — `IN_PROGRESS` — 已加入连续 popstate pending queue 与 bfcache 恢复保护；待实机 back 验证。
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
