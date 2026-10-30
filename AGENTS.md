# Starbook Agent Handoff / 必读入口

> **这是所有新 Agent、AI 编程窗口和新开发会话的第一入口。**
>
> 在修改任何代码、数据库、部署配置或产品体验之前，必须先完成本文规定的阅读顺序。不要仅凭旧对话、文件名或局部代码猜测当前架构。

## 1. 当前项目身份

- Project: **Starbook / 星屿之书**
- Current version: **1.10.2**
- Production branch: **`main`**
- Production deploy: **GitHub Pages via GitHub Actions**
- Runtime backend: **Supabase Anniversary Bridge**
- Current Book: **星屿之书** (`8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`)
- Current product preset:
  - relationship: `romantic`
  - theme: `magic-celestial`
  - experience: `world-map`
- Current delivery priority: **2026-10-29 周年纪念版稳定交付**

## 2. Agent 必读顺序

任何新 Agent 在开始工作前，按顺序阅读：

1. `AGENTS.md` —— 当前文件，确认协作规则。
2. `PROJECT_STATE.md` —— 当前真实状态、技术债、已验证能力、下一优先级。
3. `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md` —— 项目管理、开发、发布、部署、数据、回滚全链路。
4. `docs/ARCHITECTURE_EXTENSION_CONTRACT.md` —— 当前架构边界与未来扩展不可破坏约束。
5. `docs/DATA_LIFECYCLE.md` —— Supabase 数据生命周期、版本升级与迁移规则。
6. `CHANGELOG.md` —— 已完成的版本变化。
7. `ROADMAP.md` —— 未完成事项和后续方向。
8. 当前目标版本对应 `docs/releases/vX.X.X.md`。
9. 如果任务涉及场景切换、图片、播放器、编辑器、Canvas 或移动端性能，阅读 `docs/PERFORMANCE_GUIDE.md`。
10. 最后才读取与任务直接相关的源代码。

如果上述文件与旧聊天记录冲突，**以仓库当前文件为准**。

## 3. 修改前必须回答的 7 个问题

Agent 在动手前应自行确认：

1. 当前要修改的是哪一个版本？
2. 这次改动属于产品功能、稳定性、架构、数据、部署还是文档治理？
3. 是否影响 `SB.user / SB.book / SB.magicBook / SB.theme / SB.experience / SB.store` 的职责边界？
4. 是否影响 Supabase schema、RLS、Storage 或现有真实数据？
5. 是否影响 GitHub Actions、分支、PR、main 或 Pages？
6. 是否破坏多用户、多 Book、多关系、多 Theme、多 Experience 的未来兼容性？
7. 本次改动需要同步更新哪些版本记录？

如果不能回答，不应直接大规模重构。

## 4. 当前最重要的架构边界

- `SB.book` = **当前数据 Book / Book Context**，不得再用于魔法书视觉控制。
- `SB.magicBook` = **Magic Celestial 魔法书视觉与开书动画控制器**。
- `SB.store` = **业务数据兼容层**，当前内部读写 Supabase `book_data.payload`。
- `magic-celestial` 只是第一套 Theme，不等于 Starbook Core。
- `world-map` 只是第一套 Experience，不等于 Starbook Core。
- 当前是情侣书，但 Starbook Core 不得写死“情侣是唯一关系”。
- 当前 UI 只有一本 Book，但业务代码不得假设用户永远只有一本 Book。
- 当前 Memory 与 City 仍有 V1 耦合，这是技术债，不应进一步强化。

## 5. 当前数据与发布原则

### 代码生命周期

`release/*` 或 `feature/*` → PR → `validate-starbook` → merge `main` → GitHub Pages 自动部署。

### 数据生命周期

Supabase Database / Private Storage **独立于 Git 分支和 Pages 部署**。

正常前端版本升级：

- 不清空 Supabase；
- 不重新 seed Book；
- 不重新导入照片；
- 不重新导入回忆；
- 不执行破坏性 reset SQL。

数据库结构升级或 Production 数据元信息/成员变更必须使用**向前 migration**。

当前 v1.5.1 的标题与成员变更由 `supabase/migrations/002_v151_title_and_members.sql` 管理，禁止通过重跑 seed 清空或覆盖业务数据。

## 6. 每个版本强制维护的文件

每个正式版本必须同步更新：

- `VERSION`
- `CHANGELOG.md`
- `ROADMAP.md`
- `PROJECT_STATE.md`
- `docs/releases/vX.X.X.md`

如果项目管理链路、架构边界、数据策略或发布策略变化，还必须同步更新：

- `AGENTS.md`
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`
- `docs/DATA_LIFECYCLE.md`
- `docs/RELEASE_WORKFLOW.md`

`tools/check_project.py` 与 `validate-starbook` 会检查其中一部分要求。

## 7. 每个 Release Record 必须明确写出的链路变化

每个 `docs/releases/vX.X.X.md` 至少包含：

- 本版目标；
- 产品体验变化；
- Runtime / 架构链路变化；
- 数据链路变化；
- Auth / 权限 / RLS 变化；
- Storage 变化；
- Git / PR / CI / Pages 发布链路变化；
- Agent / 文档治理链路变化；
- 文件变化；
- Migration / 手动操作；
- 测试与验证；
- 已知问题；
- 回滚方式；
- 下一版本建议。

如果某一项没有变化，也必须明确写“无变化”，不能省略。

## 8. 发布前最低检查

至少执行：

```powershell
python build.py
python tools/check_project.py
```

然后通过 PR 的 `validate-starbook`。

正式 Pages 只允许 `main` 部署。

## 9. 禁止事项

除非用户明确批准并已有迁移/回滚方案，否则禁止：

- 重置 Supabase production 数据；
- 删除真实 `book_data` / Storage 文件；
- 重新运行会覆盖真实数据的 seed；
- 在前端或仓库加入 `sb_secret_`、`service_role`、数据库密码、GitHub PAT；
- 关闭 RLS 来“解决”权限错误；
- 绕过 `main` 直接让 release/feature 分支覆盖 Production；
- 无版本记录地修改 schema；
- 为了重构漂亮而破坏 2026-10-29 周年交付稳定性；
- 把 `SB.book` 与 `SB.magicBook` 再次合并；
- 将当前唯一 Theme / Experience / Relationship 写死为平台唯一能力。

## 10. Agent 交接输出格式

一个 Agent 完成工作后，应在回复或 release record 中说明：

1. 当前版本；
2. 完成了什么；
3. 修改/新增/删除了哪些文件；
4. 是否改数据库；
5. 是否需要用户手动操作；
6. 如何测试；
7. 是否影响 Production / Supabase 数据；
8. 已知问题；
9. 下一步建议；
10. 是否已经更新版本治理文档。

---

**核心原则：Starbook 的代码可以迭代，用户真实回忆数据必须持续存在；当前周年版本可以简单，但未来扩展接口不能被写死。**

## 11. 一键发布入口

版本开发完成后，不再要求 Owner/Agent 每次重新拼接 Git 发布命令。首选入口：

```powershell
.\release-current.ps1
```

规则：

- 版本号唯一来源是根目录 `VERSION`；
- 脚本自动生成缺失的 `docs/releases/vX.X.X.md` 基础记录，但 Agent 仍负责补全真实链路变化；
- 脚本自动生成 `scripts/releases/release-vX.X.X.ps1` 作为版本审计记录；
- `publish.ps1` 仍是底层发布执行器，不建议新 Agent另造发布流程；
- 数据库 migration 绝不由发布脚本自动执行。

完整说明：`docs/RELEASE_AUTOMATION.md`。

### v1.7.3 场景性能 Prompt
修改登录、魔法书、Globe、Country、City、Player 或 Scene Runtime 前，必须先阅读 `prompts/performance/` 中对应链路文件；不得绕过 `prepare → await enter → nextPaint → reveal` 生命周期。

### v1.8.0 转场 / 导航 / 搜索
- 转场视觉只能通过 `SB.gate`（`blocks/01b-gate.html`，提示词 `prompts/00-gate.md`）扩展；不得为了特效改变 Scene Runtime 事务顺序，失败路径必须调用 `SB.gate.abort()`。
- 大洲国家目录页已在 v1.8.0 删除，不要恢复 `continent` 场景；国家地图的父级是 `globe`。
- 离线城市库 `blocks/06-world-cities.html` 由 `tools/make_cities.py` 生成，不要手改；在线城市搜索只发送搜索词，不得发送任何回忆、照片或账户数据。

### v1.8.1 转场曝光 / 菜单 / 工具标识 / 时光长卷
- 新转场视觉必须遵守 `prompts/00-gate.md` 的曝光规则（全屏遮罩只用深色、亮色只是局部光源、叠加层 alpha ≤ 0.55、汇聚粒子随距离淡出）；新路线优先复用已有五种门，按「路线表」选择 `transition`。
- 菜单只放场景导航（目前「世界星图」「时光长卷」）；设置类功能（音乐、动效、账户等）注册到右上角 `SB.dock`，不要再加回菜单。
- 「时光长卷」场景 id 仍为 `overview`，不要改 id（深链与历史兼容）。

### v1.8.2 手机性能红线
- 开书动画期间不得创建 WebGL / 编译着色器（不要在 `04-book-opening` 里 `prefetch('globe')`）。
- 不要把会移动的元素放进魔法书的 3D `preserve-3d` 上下文并与书本平面相交（手机 WebKit 平面切割 → 闪烁）；需要环绕效果时用 2D 投影图层。
- 叠加混合（`lighter`）的粒子不能在同一位置持续堆积；手机档优先关闭混合模式、大面积遮罩和 SVG 光照滤镜。

### v1.9.0 搜索数据 / 编辑器扩展点 / 启动门
- `blocks/06-admin-divisions.html` 是生成文件，修改请改 `tools/make_admin.py` 并重新生成；新增国家的区划沿用同一紧凑格式。
- 照片批量操作通过 `SB.editor.photoActions` 扩展，不要在编辑器里硬编码新的批量按钮。
- 启动门动画只能用 transform / opacity；文字字体由 `data-gate-type` 一次性决定，不要在 Gate 上直接依赖网络字体。

### v1.9.1 照片分组
- 回忆的分组数据是可选字段 `groups: [{id, text}]` + 照片 `g`；组成员在 `slides` 中必须连续，编辑器的任何排序操作之后都要 `normalizeGroups(st)`。
- 放映器按 `unitsOf()` 的单元编排；新增放映风格时也必须处理组单元（组描述铺满整组时长、组内不显示单张描述、组描述为空按普通照片）。
- 放映方式（自动 / 手动）是本机观看偏好，不写入回忆数据；新增放映风格时 `holdsOf()` 自动从时间线算停靠点，描述类文字元素必须有 `t1`，否则手动模式无法在描述显示时停住。
- 地球搜索面板不显示数据来源行；数据署名放在 `README.md`「数据来源」。

### v1.9.2 镜头语言库 / 电影模式
- 新增文字样式请加入 `GEN` 并在 `animGen()` 里实现进退场（只用 transform / opacity，华丽档才允许模糊），同时在 `inEndOf()` 给出进场时长（供定格优化与手动放映停靠点使用）。
- 新增银幕镜头请在 `pickShot()` 里给出适用条件与权重，镜头内部只生成照片 / 文字元素，不要直接操作 DOM。
- 自动放映不显示进度条；放映中的按钮只能在鼠标进入底部区域或轻触时浮现，不要在开场 `wake()`。

### v1.10.0 时光之环 / 时光剪影 / 音乐 / 发布脚本编码
- 时光长卷的三维效果使用自做透视投影 + 每张卡片独立透视，**不要**改成共享的 `preserve-3d` 场景（手机 WebKit 平面切割红线）；环线必须分前 / 后两层 canvas 以保证遮挡关系。
- 周年节点由回忆日期计算（每满 12 个月），不写入数据；「时光剪影」只读回忆，所有动画用 CSS 关键帧以便暂停。
- PowerShell 脚本读取文本文件必须写 `-Encoding UTF8`（Windows PowerShell 5.1 默认按 GBK 读取无 BOM 的 UTF-8 会把中文写成乱码）；`tools/check_project.py` 会检查。

### v1.10.1 时光之环优化 / 日期精确到日 / 纪念日
- 时光长卷的卡片数量必须有上限：焦点附近（电脑左 2 右 1、手机左右各 1）才是 DOM 卡片，其余是 canvas「光珠」；不要恢复「每段回忆一张常驻卡片」或 `loading=lazy`（3D 变换下懒加载常常不触发）。
- `sb:data` 只有回忆 / 城市 / 纪念日真的变化时才允许重建时光之环（签名地址回调会频繁触发 `sb:data`，整环重建会造成闪烁）。
- 回忆 `date` 可为 `YYYY` / `YYYY-MM` / `YYYY-MM-DD`；排序、周年、分段一律用 `SB.date.day()`，不要再用字符串比较或月序号。旧数据只有年月时按当月 1 日计算。
- 周年起点是可选的 `settings.anniversary`（YYYY-MM-DD，在 `book_data.payload.settings` 内，无 schema 变化）；未设置时用最早一段回忆的日期。
- 魔法书页的场景 world 为 `night`（与其他页面同一星空深蓝背景）；金色只属于书本自身的光，不要再把整页背景做成暖金色。

### v1.10.2 时光剪影进度条 / 返回原位 / 拖动稳定 / 安卓性能
- 「时光剪影」跳转只能通过 `seekTo(T)`：重放 cue + 用 `getAnimations()` 前移新动画的 `currentTime`；新增片段时，退场类 cue 必须根据 `R.lag` 立即移除已经退场很久的元素（参考 `chapterOut`）。尾声不要再画飞出表盘的线——「未完待续」用表盘自身的语言表达（外圈新光）。
- 场景 `enter` 判断「返回」时必须同时认 `opts.back` 与 `opts.fromHistory`（从子页返回多数走浏览器历史）。
- 全局已阻止原生 `dragstart`（除 `[draggable="true"]`）；新的拖动面请调用 `SB.dragSurface(el)`、设 `user-select:none`，并在 window 上兜底 `pointerup / pointercancel`、处理 `lostpointercapture` 与 `blur`；主指针按下时清空残留指针表。
- 安卓专属降级集中在 `SB.perf.android`（见 `prompts/performance/06-android.md`）：显示尺寸代理图 `SB.store.displayUrl()`、放映 low 档只用 transform 的画内运动与等比缩放、遮罩转场换淡入淡出、全屏 canvas 像素比上限。桌面 / iOS 行为不因此改变（low 档的 transform 化对所有 low 档设备生效，视觉等价）。
