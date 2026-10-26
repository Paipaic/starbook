# Changelog

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
