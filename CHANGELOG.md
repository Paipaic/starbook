# Changelog

## [1.7.0] - 2026-10-26

### Added
- **「光影放映」多图编排放映引擎**（VIS-005）：每种风格是一位「导演」，把照片编排成声明式时间线；画面里常有 2–3 张照片**接力**更替（一张留着、一张渐隐、新的一张渐显），不再一页一张。单张焦点约 3.2–3.6 秒，只有描述较长时才多停留。
- **三种放映风格**：
  - 银幕（默认）：宽银幕全幅镜头 + 双联 / 三联分屏；光缝、虹膜、百叶、擦入、光晕溶解、错位竖条、面板扩展为全幅、像门一样向两侧打开等转场；分屏中正在讲述的照片提亮；短句竖排大字幕、长句下三分之一大字幕（字距收拢 + 逐字去模糊 + 金线）。
  - 星图：星空中 2–3 张烫金相框前后漂浮、视差与轻微 3D 倾斜，接力更替时旧照片化作星尘、新照片光晕显影，金线把相邻照片连成星座；字幕为编辑式大号编号 + 逐行遮罩升起。
  - 手札：烛光皮革书桌，相片逐张从空中落下（回弹 + 阴影 + 微尘）、堆叠，镜头沿桌面跟随最新相片；旁白像羽毛笔逐字写出（湿墨金光渐干），火漆星章点缀。
- **四季主题**（VIS-006）：春（樱花瓣翻飞、粉桃柔光）、夏（阳光光束、萤火）、秋（枫叶翻滚、琥珀暖调）、冬（三层雪花、银蓝霜边）；放映厅与放映控制条可临时切换，粒子与调色交叉渐变；按月份自动选择季节。
- 回忆**可选字段** `style`、`season`（缺省 `cinema` / `auto`）。
- 放映厅新增「STYLE / SEASON」选项（只影响本次观看）与随风格变化的预计时长。
- `SB.cinema`（风格 / 季节定义与图标）；`SB.player.setStyle / setSeason / stepSeason / estimate`。

### Changed
- **回忆编辑器升级为「星屿手稿」**（VIS-007）：左侧实时海报预览（封面、标题、日期、地点、风格 / 季节徽章、季节调色与飘落预览、照片数与预计时长）；右侧四章——Ⅰ 故事、Ⅱ 影像（照片卡片网格，直接在卡片上写描述，前移 / 后移 / 封面 / 移除）、Ⅲ 放映（三张带循环示意动画的风格卡片 + 季节选项）、Ⅳ 乐章。手机为单列。
- 扉页标题与一段话字号加大；扉页最长 9 秒。
- 跳转（上一张 / 下一张 / 进度条）改为跳到照片焦点时刻，并用 0.5 秒暗场衔接。
- `prompts/11-memory-player.md`、`prompts/12-memory-editor.md` 重写；`docs/design/VISUAL_UPGRADE_PLAN.md` 新增第 7 节调研与候选对比；转场与魔法书 / 地球特效顺延为 v1.7.1 / v1.7.2。

### CI / Governance
- `tools/check_project.py` 放映回归检查增加 `SB.cinema`。
- 新增版本发布脚本 `scripts/releases/release-v1.7.0.ps1`。

### Data
- **不需要运行 SQL，不改 schema_version，不迁移旧数据。** 新字段只在编辑并保存回忆时写入；旧回忆按默认风格 / 按月份季节放映。

## [1.6.0] - 2026-10-26

### Added
- **「冥想盆放映厅」电影式回忆放映**（VIS-004）：
  - 放映厅：封面海报（烫金细框）、日期 / 标题 / 地点、照片张数与预计时长、带旋转符文环的「放映」按钮。
  - 开场：熄灯与放映机启动闪烁、银幕黑边落下（横屏约 1.85:1，竖屏 7% 画框）、墨滴入水 + 三圈涟漪、扉页逐字浮现。
  - 镜头：按照片比例自动选择推镜 / 拉镜 / 横摇 / 纵摇 / 悬浮相片，正弦缓动，放大不超过 1.12。
  - 转场：光尘溶解（默认 1.6s）、暖金光漏（每 4 个镜头与最后一个镜头）、墨滴揭幕（第一张）；手动翻页 0.8s。
  - 电影字幕：按 Netflix 简体中文规范（每行 ≤16 字、≤2 行、金字塔断行），按每秒 7 字计时，逐字柔和浮现；照片停留时间自动延长到字幕读完。
  - 终章：暖金闪白 → 「终 · FINIS」、日期地点、「再放一遍 / 返回相册」；音乐 3 秒内渐弱到 30%。
  - 胶片颗粒、暗角、金色光尘；分段进度条可点击跳转；滑动 / 键盘 / 空格控制；切到后台自动暂停。
- 城市相册卡片右下角新增「放映」按钮，直接开始放映。
- `SB.audio.duck(level, ms)` 音量平滑压低 / 恢复。
- `SB.player`（play / seek / jump / state）供测试与调试。

### Changed
- `prompts/11-memory-player.md` 重写为 v1.6.0 放映提示词；`docs/design/VISUAL_UPGRADE_PLAN.md` 新增第 6 节电影式放映参数调研。
- 照片等待签名地址最多 5 秒，期间显示「正在冲洗胶片…」，并预加载解码后续照片。
- 低性能（动效「柔和」）去掉模糊与胶片颗粒；系统「减少动态效果」只保留淡入淡出。

### Data
- **无数据库、RLS、Storage 变化；无需运行 SQL；只读取已有回忆字段，不影响任何已有回忆数据。**

### CI / Governance
- 新增 `release-current.ps1`：以后完成版本迭代后只需从 `VERSION` 自动识别版本并一键进入发布链路。
- 自动生成缺失的 `docs/releases/vX.X.X.md` 基础记录，以及版本审计脚本 `scripts/releases/release-vX.X.X.ps1`；已有 Release Record 不覆盖。
- `publish.ps1` 在被直接调用时也会从模板补齐缺失 Release Record，修复“required governance/release files missing”发布中断。
- `check_project.py` 的 `OK` 改为所有治理校验真正通过后才输出，并增加旧 `data/db.json` / GitHub runtime persistence / `SB.book` 视觉对象回流硬保护。

## [1.5.2] - 2026-10-26

### Fixed
- **字体“乱码”根因修复**：移除 ZCOOL XiaoWei。该字体的「回 圃 圄 圊 崮 徊」字形自身损坏，在 Chromium / FreeType 下渲染为实心方块，导致「回忆总览」等显示为「■忆总览」；且只覆盖约 7000 字，罕见字会混入其他字形。
- 移除 Cinzel Decorative：数字「1」显示为罗马式「I」，小字号花体难以辨认。
- `✦ ✎ ✕ ⟲` 等在网页字体中不存在的符号全部改为内联 SVG 图标，手机上不再回退成 Emoji 或空心方框。
- 标题中的分隔点「·」不再出现在行首。

### Added
- 「星文」字体系统：中文统一思源宋体（Noto Serif SC 400/600，封面书名 900 按字子集加载）、拉丁铭文 Cinzel、数字与日期 Cormorant Garamond。
- 排版令牌：字号阶梯 `--fs-*`、行高 `--lh-*`、字距 `--tr-*`、字重 `--fw-*`；`.sb-num`、`.sb-rune`、`.sb-foil` 工具类。
- `SB.icon(name)` 内联 SVG 图标集（spark / star / quill / close / reset / plus / minus / up / down / chevron / note）。
- `SB.ui.button(text, kind, onClick, icon)` 可选图标参数（向后兼容）。
- `SB.fmtTitle()` 标题分隔点防断行；`SB.type.ready` 字体预热。
- `docs/design/VISUAL_UPGRADE_PLAN.md`：v1.5.2 → v1.6.2 视觉升级计划、乱码实测与调研来源。
- `prompts/00-typography.md`：字体系统提示词。

### Changed
- 所有场景标题、按钮、标签、菜单、提示条、弹窗改用 `--f-display`；居中大字距标题增加光学居中补偿。
- 总览统计、时间线日期、放映页码等数字改用 Cormorant Garamond 等高数字。
- 魔法书封面 SVG 文字改用思源宋体 900 / Cinzel，铭文分隔改为 `·` 与绘制的四芒星。
- Supabase 客户端 `x-client-info` 改为读取运行时配置版本号。

### CI / Governance
- `tools/check_project.py` 新增字体回归检查：构建产物中出现 ZCOOL XiaoWei、Cinzel Decorative 或 `✦ ✎ ✕ ⟲` 时校验失败；并检查 `SB.icon` 存在。

### Data
- **无数据库、RLS、Storage 变化；无需运行 SQL；不影响任何已有回忆数据。**

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
