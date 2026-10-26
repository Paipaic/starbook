# Changelog

## [1.5.1] - 2026-10-26

### Added
- 根目录 `README.md`，为 GitHub 与人工阅读提供简短入口，并明确新 Agent 从 `AGENTS.md` 开始。
- `supabase/migrations/002_v151_title_and_members.sql`：非破坏性更新当前 Book 标题，并加入两名 `editor` 成员。
- 当前 Book 新增 editor：`11aa32fe-3875-4880-81fb-02a543dca853`。
- 当前 Book 新增 editor：`62adee54-c59a-4844-abb5-1b5629da3bf9`。
- 根目录 `AGENTS.md`，作为所有新 Agent / 新开发会话的强制上下文入口。
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`，固化需求 → 分支 → 校验 → PR → main → Pages → 数据保留 → 回滚的完整项目链路。
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`，固化多用户、多 Book、多 Relationship、多 Theme、多 Experience 的长期扩展边界。
- `docs/DATA_LIFECYCLE.md`，明确 Git/Pages 与 Supabase 数据生命周期分离以及向前 migration 原则。
- `docs/PROJECT_DOCS_INDEX.md` 与 `docs/templates/RELEASE_RECORD_TEMPLATE.md`。
- `docs/V151_OPERATOR_STEPS.md`，明确本次发布、Supabase migration 与 Production smoke test 的 Owner 操作。
- `docs/releases/v1.5.1.md` 完整 Release Record。
- 正式纳入 `validate.yml`、`deploy-pages.yml` 与 `publish.ps1` 的长期发布链路说明。

### Changed
- 当前 Anniversary Book 展示名称由《我们的星屿》统一为《星屿之书》，包括 Supabase `books.name`、登录权限提示、初始化 seed 与当前项目文档。
- `main` 正式定义为唯一 Production branch；release/feature 分支只通过 PR 进入 main。
- 每个版本必须记录 Product、Runtime、Architecture、Data、Auth/RLS、Storage、CI、Git/PR、Pages、Agent Governance 等链路变化；无变化也必须显式声明。
- 发布检查升级为“代码 + 文档治理”双重校验。

### Fixed
- 修复 Windows PowerShell 下 `publish.ps1` 的 Secret 扫描：`site/.nojekyll` 等空文件会让 `Get-Content -Raw` 返回 `$null`，此前会在 `.Contains()` 处中断发布。现仅扫描文本资源并显式跳过空内容。

### CI / Governance
- `tools/check_project.py` 开始检查 VERSION、Release Record、CHANGELOG、PROJECT_STATE 和核心治理文档一致性。
- `validate-starbook` 在 PR 上执行 build、项目检查和高风险 Secret 扫描。
- `publish.ps1` 发布前要求当前版本文档完整，避免无记录发布。

### Data
- **无 schema 结构变化，`schema_version` 保持 1。**
- 发布 v1.5.1 后需运行一次 `supabase/migrations/002_v151_title_and_members.sql`。
- Migration 仅更新 `books.name` 并 upsert 两名 editor；**不会修改 `book_data.payload`，不会删除/重建 Storage，不需要重新导入城市/回忆/照片/BGM。**
- Supabase 现有数据继续由同一 Book ID / Private Storage 承载。

## [1.5.0-anniversary] - 2026-10-26 (in progress)

### Added
- Supabase Anniversary Bridge 基础架构。
- `SB.user`、`SB.book`、`SB.theme`、`SB.experience` Runtime Context。
- Email + Password 私有登录门；周年版不开放公众注册。
- `books` / `book_members` / `book_data` Supabase schema 与初始化 SQL。
- Private Storage `starbook-media` 与基于 Book Membership 的 RLS。
- Private Storage Signed URL 内存缓存。
- `book_data.revision` 轻量并发冲突检测。
- 浏览器 `pushState` / `popstate` 场景历史支持。
- 版本文件、Roadmap、Project State 与 Release Record 制度。

### Changed
- `SB.store` 从 GitHub PAT / GitHub Contents & Git API 改为 Supabase Bridge Store。
- V1 `cities / memories / settings` JSON 数据结构保持不变，改存于 `book_data.payload`。
- 图片和音乐改为按 `{book_id}/images`、`{book_id}/audio` 保存到 Private Storage。
- 音乐周年版改为直接上传常见格式，不再浏览器转码。
- App 启动改为 Auth → Book Context → Store Ready → Scene Boot。

### Removed
- 周年正式运行路径中的 GitHub PAT 编辑钥匙。
- GitHub 仓库作为运行时数据库/媒体存储的依赖。
- `mp4-muxer` 音乐转码依赖。

### Security
- 浏览器端仅配置 Supabase Publishable Key。
- 未认证用户无法通过 RLS 读取 Book Data 或 Private Storage。
- Owner / Editor / Viewer 权限开始由 `book_members` 决定。

### Pending Verification
- Supabase migration / owner seed / Private Bucket 已在真实 Project 中执行并确认。
- 仍需真实 Auth 登录、前端 RLS、Storage 上传与手机端测试。

### Phase 3 Stability
- 移动端全局高度改为 `100dvh` 优先，并加强 safe-area / coarse pointer 触控目标。
- 动态脚本加载增加单源超时机制，Three.js 扩展为 cdnjs / jsDelivr / unpkg 三源回退，避免单个 CDN 长时间挂起。
- 浏览器 / Android 连续返回增加 pending history 队列；转场期间产生的新 `popstate` 会在当前动画结束后追到最终历史状态。
- bfcache / 系统返回恢复时主动清理遗留 `is-busy`、veil、flash 状态，降低整页突然无法点击的风险。
- 地球与国家地图在触控设备上提高“点击 vs 拖动”判定阈值，降低手指拖动造成误进入国家 / 地区。
- 手机导航、菜单与通用按钮扩大最低触控尺寸。

### Reliability
- Private Storage Signed URL 增加失败后的自动补签与去重机制。
- 增加 `SB.store.health()` 轻量诊断接口，便于周年版实测定位 Database / Storage 权限问题。


### Fixed
- **Auth recovery hotfix:** 登录错误状态不再统一落入“重新连接”死路。密码/凭据错误保持在登录表单内提示；无 Book 权限和 RLS/数据库访问异常增加“返回登录”出口。
- “返回登录”会退出当前 Supabase Session、清空当前 Book Context 并回到登录表单，无需刷新页面。
- **Phase 2 interaction hotfix:** 修复 Runtime Book Context 与 V1 魔法书视觉控制器同时使用 `SB.book` 导致的全局命名覆盖。现在 `SB.book` 仅表示当前数据 Book，魔法书封面/开书动画改为 `SB.magicBook`。
- 修复该冲突引发的 Store 无法稳定取得 `book_id / role`、登录后场景交互异常风险。
- 修正 Anniversary Bridge SQL：移除周年版非必要的自定义 helper function，改用直接 RLS membership 判断，降低迁移兼容风险。
