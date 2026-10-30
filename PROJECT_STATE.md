# Starbook Project State

## Current Release

- Version: `1.10.2` (时光剪影进度条与尾声 · 返回原位 · 拖动稳定 · 安卓性能)
- Deadline: `2026-10-29`
- Delivery goal: 私密、稳定、手机可用的周年纪念礼物。
- Base: V1 `blocks + build.py + site/index.html`。
- Runtime config version: `1.10.2`。

## Current Architecture

Frontend: GitHub Pages 静态页面。

Backend: Supabase Lite / Anniversary Bridge：
- Auth: Email + Password
- Database: `books`, `book_members`, `book_data`
- Storage: private bucket `starbook-media`
- Realtime: **not enabled for anniversary release**
- PWA: **not enabled for anniversary release**

## Runtime Context

- `SB.user`: 当前登录用户 / Session。
- `SB.book`: 当前数据 Book 与用户角色（Supabase Runtime Context）。
- `SB.magicBook`: Magic Celestial 封面与开书动画控制器；不得与 `SB.book` 合并。
- `SB.theme.current`: 当前 `magic-celestial`。
- `SB.experience.current`: 当前 `world-map`。
- `SB.store`: V1 兼容数据接口，内部读取 `book_data.payload`。

Current Book:
- id: `8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`
- name: `星屿之书`
- relationship: `romantic`
- theme: `magic-celestial`
- experience: `world-map`

## Anniversary Bridge Data

`book_data.payload` 当前继续保存 V1：

```json
{
  "cities": {},
  "memories": {},
  "settings": {}
}
```

这是临时兼容层，不是最终 V2 数据模型。

`revision` 用于轻量并发冲突检测。

## Storage Convention

Private bucket: `starbook-media`

```text
{book_id}/images/{generated-id}.jpg
{book_id}/audio/{generated-id}.mp3|m4a|...
```

媒体属于 Book，不属于单个 User。

## Architecture Invariants

1. Starbook 必须保留多用户扩展能力。
2. 一个用户未来可以拥有或加入多本 Book。
3. 一本 Book 可以有多个成员。
4. 不允许业务代码假设系统永远只有一本 Book。
5. 不允许 Starbook Core 假设所有 Book 都是情侣关系。
6. Relationship Type 与 Theme 独立。
7. Theme 与 Experience 独立。
8. `magic-celestial` 只是第一套 Theme。
9. `world-map` 只是第一套 Experience。
10. Memory 未来不得强制要求 Location / City。
11. Book 内业务数据必须有明确 Book 所属关系。
12. 当前未开放的未来能力优先通过配置关闭，而不是破坏扩展接口。
13. 2026-10-29 前，周年版稳定性高于架构纯洁度和功能数量。
14. 不为周年版引入 React / Vue / Vite 大迁移。
15. 不在浏览器或仓库中放 Supabase Secret / service_role / 数据库密码。

## Project Governance / Agent Handoff

从 v1.5.1 起，项目上下文与管理链路正式固化在仓库内：

- `AGENTS.md`: 新 Agent 必读入口。
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`: 开发 → 校验 → PR → main → Pages → 数据保留 → 回滚全链路。
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`: 多用户 / 多 Book / Relationship / Theme / Experience 长期扩展契约。
- `docs/DATA_LIFECYCLE.md`: Supabase 数据生命周期与 migration 规则。
- `docs/RELEASE_WORKFLOW.md`: 版本发布操作说明。
- `docs/releases/vX.X.X.md`: 每版本必须记录 Runtime、数据、CI、部署和治理链路变化。

Production governance:

```text
release/vX.X.X or feature/*
→ Pull Request
→ validate-starbook
→ merge main
→ Deploy Starbook to GitHub Pages
```

`main` 是唯一 Production branch。普通代码发布不重置 Supabase 数据。


## Reel Seek / Return Position / Drag Robustness / Android (v1.10.2)

- `14-year-reel`：`seekTo(T)`（重放 cue + Web Animations 前移）、进度条 `.yr-bar`（WAI-ARIA slider：章节刻痕、拖动、键盘）、放完后「继续」从头；尾声「年轮合拢」（彗星、回忆星环、外圈新光），删除了旧的 `.tail` 引申线。
- `13-overview`：`enter` 认 `back || fromHistory` 恢复离开时的站点；重建时重置 `S.near`；window 级 `pointerup/cancel` 兜底、`lostpointercapture`、`blur`；动画循环 try/catch。
- `00-core`：全局 `dragstart` 拦截、`SB.dragSurface()`、`SB.perf.android`。`07-globe`：大洲徽章按下也能拖动地球、主指针清空残留指针、徽章尺寸缓存、安卓像素比 1；`09-country-map` 同样的指针自愈。
- `05-store`：`displayUrl(id, side)` / `proxyOn()` / `displaySide()`（安卓显示尺寸代理图，并发 3，最多 160 张，回收未使用的）。`11-memory-player`：安卓用代理图、low 档画内运动与等比尺寸只用 transform、安卓遮罩转场换淡入淡出、预载引用到离开放映。`01-ambient-fx` / `01b-gate`：安卓像素比上限。

## Ring Timeline Tuning / Day Dates / Anniversary (v1.10.1)

- `SB.date`（`00-core`）：`parse / day / str / dot / addYears / daysIn / valid / hasDay / today`。回忆 `date` 可为 `YYYY-MM-DD`（编辑器新增「日」，可选「不记得哪天」）；旧 `YYYY-MM` 照常有效，按当月 1 日排序。`SB.fmtDate` 有日则显示到日。
- `settings.anniversary`（可选，`YYYY-MM-DD`，`book_data.payload.settings`）：时光长卷标题下的「纪念日」徽记（编辑者可设置 / 恢复默认）。周年节点 = 纪念日每年同一天（2/29 平年落 2/28），≤ 今天；第一年包含纪念日之前的回忆；同一天的回忆属于新的一年。
- `13-overview`：窗口化卡片（电脑左 2 右 1、手机左右各 1）+ canvas 光珠；鱼眼弧长 `arcs()`；点击光珠 / 卡片 / 节点 / 刻度 → `center(i)` 定时缓动直达（≤ 1.25 s，远距离途中卡片收起）；图片窗口预取 + 解码淡入；`sb:data` 签名比对后才重建；静态环线缓存到离屏画布，光晕用贴图；延伸线顺环外旋、渐虚，笔尖光点 + 沿线文字。调试接口 `SB.overview.state / center / hitPoint`。
- `14-year-reel`：`from / to` 为 `YYYY-MM-DD`；表盘位置按日计算；超时后迟到的照片不再改写「正在准备」提示。
- `03-magic-book`：场景 world `night`、粒子 `night`、星云改为蓝紫色。

## Ring Timeline / Year Reel / Music (v1.10.0)

- `13-overview`：站点 = 起点节点 + 回忆 + 周年节点（每满 12 个月）+ 「此刻」节点；自做透视投影（`proj()`），环线画在前 / 后两层 canvas，悬挂卡片按纵深设置层级与透明度；场景激活时持续运行动画循环（柔和档 30fps，静止档只在拖动时运行，页面隐藏时停止）。调试接口 `SB.overview.state / center(i)`。
- `14-year-reel`（新块）：`SB.yearReel.open({year, from, to, list, now})` / `close()`；所有动画为 CSS 关键帧，JS 只在时间点切换状态；照片先预载（最多 8 秒）。
- `SB.audio`：数据就绪即尝试自动播放；点击 / 轻触 / 按键解锁；ended / error / visibilitychange 自动恢复。
- 发布脚本读取文件显式 UTF-8；`check_project.py` 检查文档乱码。

## Screening Language (v1.9.2)

- 文字元素新增 look：`title / poem / quote / whisper / note / stamp`（`GEN` 集合，由 `animGen()` 驱动进退场），`cinema` 支持 `in:'spark'`；字段 `kick`（幕序 / 编号）、`drift`（视差）、`outDur`、`right`、`deco`（装饰文字，不参与停靠点）。
- 照片元素新增画框 `arch / mat / soft(+side)`，进退场 `zoom / rise / develop / sink`，互动 `rack`（虚焦 / 压暗），手札装饰 `deco: tape | tapeb | clip`。
- 银幕 `pickShot()` 镜头选择；组单元 `board`（故事板）。星图 `HERO` 页；手札便笺 / 邮戳。
- 自动放映：`start()` 预载；`data-mode` 控制进度条；`zoneH()` 底部浮现。

## Photo Groups (v1.9.1)

- 回忆数据新增可选 `groups: [{id, text}]` 与照片 `g`（组 id），存于 `book_data.payload`，无 migration。
- 编辑器维持组成员在 `slides` 中连续（`normalizeGroups`）；批量操作 `group` / `ungroup` 注册在 `SB.editor.photoActions`；注册表 `label` 可为函数。
- 放映器 `unitsOf()` 把照片切成单元，三种导演分别编排组单元；组描述为空的组按普通照片放映。
- 放映方式：`P.mode = auto | manual`（localStorage `sb-play-mode`）；`buildTL()` 产出 `holds`（停靠点），手动模式时钟在停靠点停住，`advance()` 翻页（3 倍速 rush 到下一张或直接跳转）。

## Search / Editor / Gate (v1.9.0)

- 地球搜索：`SB.ADMIN_DIVISIONS`（`blocks/06-admin-divisions.html`，`tools/make_admin.py` 从 Vonng/adcode、btskinner/spatial、kjhealy/fips-codes 本地克隆生成）。中国区划基线 2016、美国县 2010。
- 编辑器：`SB.editor.photoActions` 批量操作注册表；上传并发 2；删除可撤销（文件仍在保存时清理）。
- 登录门：`html[data-gate-type="web|local"]` 一次性字体决策；动画只用 transform / opacity；`SB.fx.start()` 移到 `store.ready` 之后。

## Book Opening (v1.8.3)

- 开书 = 机关启封（`SB.magicBook.awaken(on)` / `unlock()`，1.9s）→ 启封（`fxOpen`，扉页金墨星图 + 星尘）→ 入页 → 门钥匙。详见 `prompts/04-book-opening.md`。
- 只用 transform / opacity / 短时描线；小齿轮 SVG 自转只在机关启动的 2 秒内对所有档位开启。

## Mobile Performance (v1.8.2)

- 开书期间禁止创建 WebGL（不调用 `SB.scenes.prefetch('globe')`）；地球在门钥匙盖满后准备。
- 魔法书符文环是 2D 投影的前 / 后两层（`#bk-runes-front` / `#bk-runes-back`），不得放回 3D `preserve-3d` 上下文（手机 WebKit 会切割相交平面导致闪烁）。
- 柔和档（手机默认）关闭昂贵的混合模式 / 遮罩层并使用廉价烫金滤镜；薄烟只在华丽档、正常混合。
- 皮革 / 纸张纹理缓存在 localStorage；放映器纹理延迟生成。
- 右上角标识组新增「回到魔法书」（`SB.dock` 的 action 类标识）。

## Visual / Layout (v1.8.1)

- 转场按路线区分（`SB.gate.kinds = portkey / nox / quill / pensieve` + `portal` 装饰）：`flash`=门钥匙（书 / 菜单 → 地球）、`portal`=幻影显形（地球 → 国家）、`quill`=墨金书页（→ 城市、→ 时光长卷）、`pensieve`=冥想盆（→ 放映）、`veil`=熄灯器（返回）。曝光规则见 `prompts/00-gate.md`。
- 魔法书材质「星夜摩洛哥皮」：午夜靛蓝皮革、香槟古金、盲压花边、镶嵌星辰、古金包角（`blocks/03-magic-book.html`）。
- 菜单只有「世界星图」「时光长卷」；音乐 / 动效 / 账户在右上角 `SB.dock`（`blocks/02y-dock.html`，各块用 `SB.dock.add` 注册面板）。全站背景音乐管理在音乐面板里。
- 「时光长卷」（场景 id 仍为 `overview`）：横向可拖动时间轴；放映参数 `from:'overview'` 时返回到时光长卷。
- 城市空状态：与章节卡片同比例的空白章节卡。

## Visual / Navigation (v1.8.0)

- 场景流程：魔法书 → 世界星图（地球 + 搜索栏）→ 国家地图 → 城市目录 → 回忆放映。**大洲国家目录页已删除**；国家的父级是 `globe`，返回时地球自动转向该国家。
- 转场 `SB.gate`（`blocks/01b-gate.html`）：`flash` = 门钥匙、`portal` = 幻影显形装饰、`veil` = 熄灯器 / 荧光闪烁；只替换 cover / reveal 视觉，Scene Runtime 事务不变；缺失时回退旧视觉，异常 `abort()`。
- 搜索：`SB.WORLD_CITIES`（648 城离线库，`tools/make_cities.py` 生成）+ Open-Meteo Geocoding 在线搜索（唯一新增外部服务，失败降级）；`SB.globe.focus(o)` / `SB.globe.search(q)` 供调试。
- 魔法书「星辉层次」：星云、宝石光溢 / 光束、3D 符文环、烟雾火星画布、书页边缘流光；`SB.magicBook.fxSuck(on)` 用于开书吸入。
- 地球「星辉层次」：海面高光、云雾层、外层光晕、星座线、星盘环、足迹光弧。
- 提示词：`prompts/00-gate.md`、`prompts/03-magic-book.md`、`prompts/07-globe.md`、`prompts/09-country-map.md`；调研：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 8 节。

## Scene Runtime / Performance Baseline (v1.7.3)

- Scene 生命周期：`prepare → cover → await enter → nextPaint → reveal → cleanup`。
- `SB.scenes.prefetch(id, params)` 只预热，不改变当前场景。
- 登录 Gate 必须等 `SB.store.ready + scenes.boot(book) + first paint` 后再揭开。
- Store 启动只读取 JSONB，不全量签整本书媒体 URL。
- Globe / Country / City / Player 都应在揭示前准备首屏关键资源。
- 对应逐链路 Prompt 位于 `prompts/performance/`。

## Visual / Typography (v1.5.2)

- 中文全站统一 Noto Serif SC（思源宋体）；拉丁铭文 Cinzel；数字 Cormorant Garamond；均来自 Google Fonts。
- ZCOOL XiaoWei 与 Cinzel Decorative 已移除（字形损坏 / 数字难辨），`tools/check_project.py` 防回归。
- 图标统一用 `SB.icon(name)` 内联 SVG，不依赖系统符号字体。
- 视觉升级后续版本计划：`docs/design/VISUAL_UPGRADE_PLAN.md`（v1.6.0 电影式放映、v1.6.1 转场、v1.6.2 魔法书/地球特效）。

## Visual / Cinematic Player (v1.6.0)

- 回忆放映 = 放映厅（海报 + 放映按钮）→ 开场（熄灯、银幕黑边、墨滴涟漪、扉页）→ 镜头（推/拉/横摇/纵摇/悬浮相片，溶解 / 光漏 / 墨滴揭幕转场，电影字幕）→ 终章（闪白、「终 · FINIS」、再放一遍）。
- 由单一时钟驱动，暂停即冻结；只读现有 memory 字段（title / date / note / cover / slides / bgm / bgmMode），无数据变化。
- 相册卡片右下角「放映」按钮直接开始放映；点卡片其他位置进入放映厅。
- `SB.audio.duck(level, ms)`：终章音乐渐弱到 30%；`SB.player`：调试/测试用的 play / seek / jump / state。
- 提示词：`prompts/11-memory-player.md`；调研：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 6 节。

## Visual / Multi-photo Player · Styles · Seasons (v1.7.0)

- 放映由「导演」编排成声明式时间线（照片 / 文字 / 连线 / 光漏元素 + 关键帧），渲染器只按时钟 T 计算 → 可暂停、可 seek；画面里常有 2–3 张照片接力更替。
- 三种放映风格：`cinema` 银幕（默认：全幅 + 双联 / 三联分屏、光缝 / 虹膜 / 百叶 / 擦入 / 扩展 / 开门转场、竖排大字幕）、`constellation` 星图（星空中烫金相框接力 + 星座连线 + 编辑式编号字幕）、`journal` 手札（烛光书桌、相片落下堆叠、镜头跟随、墨迹手写旁白）。
- 四季主题：春樱 / 夏光萤 / 秋枫 / 冬雪 + 调色；放映厅与放映控制条可临时切换。
- 回忆新增**可选**字段 `style`、`season`（Theme 表现偏好，缺省 = `cinema` / `auto`），无 migration、不改 schema_version。
- 回忆编辑器升级为「星屿手稿」：实时海报预览 + 故事 / 影像 / 放映 / 乐章四章。
- `SB.cinema`：风格 / 季节公共定义；`SB.player` 新增 `setStyle / setSeason / estimate`。
- 提示词：`prompts/11-memory-player.md`、`prompts/12-memory-editor.md`；调研：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 7 节。

## Visual / City Album (v1.7.1)

- 城市回忆目录（块 10）改为单列金色时间线 + 章节卡片：罗马数字章节徽记、烫金海报（风格 / 季节徽章与季节调色）、标题、照片数与预计放映时长、一段话摘录、照片缩影条，卡片上直接「放映 / 放映厅 / 编辑」。
- 页眉：缓慢旋转的法阵、城市名、统计胶囊（回忆数 / 照片数 / 时间跨度）、「新的回忆」按钮；时间线末尾「写下第 N 章」；空状态改为深色烫金「空白章节」。
- 只读现有字段，无数据变化；提示词 `prompts/10-city-album.md`，调研 `docs/design/VISUAL_UPGRADE_PLAN.md` 7.6 节。

## Performance / Responsive Baseline (v1.7.2)

- 场景切换：`portal` 不再把旧场景保持 active 到动画结束；veil / flash / portal 按设备性能缩短时长，并在 scene swap 后等待浏览器完成 paint，减少残影与卡帧。
- 性能档：综合 viewport、coarse pointer、CPU core、device memory 判定 `high / low / reduced`；low 档降低全局粒子数量、Canvas DPR 与动画刷新率。
- 放映：播放器 low / mobile 档约 30 FPS；播放期间 Ambient FX 自动降帧；进入放映厅前预热 Signed URL 与前几张照片，播放中预取 12–16 秒窗口。
- 城市目录：首屏封面优先，其他海报 / 缩影 lazy；手机减少缩影并启用 `content-visibility:auto`，降低长列表布局、图片下载与解码压力。
- 编辑器：照片网格 lazy decode；桌面 / 手机重新约束编辑器宽度、海报与照片卡片比例；窄屏照片卡片改为单列，避免可编辑区域过小。
- 新上传 Private Storage 媒体使用唯一文件名 + 长缓存元数据；不会修改旧对象或现有数据。
- 性能约束文档：`docs/PERFORMANCE_GUIDE.md`。

## Known Technical Debt

- `book_data.payload` 是整体 JSONB，后续需要正规化。
- Memory 当前仍与 City 强耦合。
- Theme / Experience 目前只有 Context，没有插件加载器。
- Signed URL 仅做内存缓存；刷新后重新签名。
- 核心 Third-party CDN 尚未全部本地化（Google Fonts 仍为外部依赖；加载失败时回退系统宋体，版式不变）。
- 完整深层 URL Router 尚未实现。
- 暂未使用 Realtime。
- 图片仍是单一压缩尺寸。

## Live Supabase Status

Confirmed by owner on 2026-10-26:
- `001_anniversary_bridge.sql`: executed successfully.
- `002_anniversary_owner.sql`: executed successfully.
- Book seed query returned one row.
- `starbook-media`: confirmed `public = false`.

v1.5.1 planned forward migration:
- `002_v151_title_and_members.sql`: run after the v1.5.1 code release (or before final verification).
- Updates Book display name to `星屿之书`.
- Adds active editor `11aa32fe-3875-4880-81fb-02a543dca853`.
- Adds active editor `62adee54-c59a-4844-abb5-1b5629da3bf9`.
- Does **not** modify `book_data.payload` or Storage.

## Core live interaction verification

Confirmed by owner on 2026-10-26:
- Production URL can open successfully.
- Auth login / auth recovery paths work.
- Magic Book scene opens correctly.
- Globe drag and continent/country interactions work.
- Current mobile / back-navigation stability test has no observed blocker.

## Phase 2 interaction hotfix

- 已修复 `SB.book` 命名冲突：V1 魔法书动画控制器已重命名为 `SB.magicBook`。
- 原因：Runtime 多 Book Context 与 V1 视觉控制器曾覆盖同一全局命名空间，可能导致 Store 取不到当前 Book 并造成登录后交互异常。
- 修复后必须重新验证：登录 → 魔法书 → 地球拖拽 → 大洲 → 国家。

## Auth / Access Recovery Hotfix

- 密码或凭据错误：保留在登录表单，允许立即修改后重试。
- 已认证但没有当前 Book Membership：提供“重新检查权限”和“返回登录”。
- RLS / 权限 / Database 异常：提供“重新尝试”和“返回登录”，避免错误页锁死用户。
- “返回登录”会 sign out 当前 Supabase Session，并清空 `SB.book` Runtime Context。

## Phase 3 Stability Hardening

- 全局视口优先使用 `100dvh`，保留 `100vh` fallback。
- coarse pointer 下通用按钮、导航和菜单扩大触控目标。
- `SB.loadScript()` 增加单源超时与自动 fallback。
- Three.js 当前保留三 CDN fallback；本地 vendor 化仍是后续可选优化，不阻塞周年交付。
- 场景历史加入 `_pendingHistory`，连续 Android / 浏览器返回时以最后一次 history state 为准。
- bfcache 恢复会清理可能残留的 busy / veil / flash。
- Globe / Country Map 在触控设备上使用更宽松的拖动阈值，减少误触。

## Highest Priority Next

1. 发布 v1.10.2（`.\release-current.ps1`），实测：时光剪影拖动进度条、看完尾声；从时光长卷点进回忆再返回停在原位；地球 / 时光之环长时间转动不再卡住；安卓手机转场与放映是否顺滑（尤其 30 张以上照片的回忆）。v1.10.1 项：时光长卷不再闪烁、卡片图片都能出来；点击远处光珠直接转到；在「纪念日」徽记设置纪念日后周年节点按日重算；给旧回忆补上具体日期后按日排序；魔法书页背景为星空深蓝；时光剪影放映中不再出现「正在准备」文字。
2. 后续：v1.11.0 地球省 / 州矢量边界与局部高清（GLB-001），v1.11.1 国家地图「星图手稿」（MAP-001）。
3. 完成 Private Storage 正式照片与 BGM 的实际内容填充，并优先使用 v1.7.2 之后的新上传缓存策略。
4. 核心稳定后实现周年扉页 / 献词 / 结尾（ANN-008）。
5. 进行最终手机端 Production URL 验收；重点观察弱网照片等待、发热、掉帧与页面残影。
6. 2026-10-28 晚 Feature Freeze；v1.8.0 之后只修 bug。若真机上新转场卡顿，可在菜单「动效强度」选择柔和 / 关闭（reduced 档不显示门）。

## Release Automation (v1.6.0+)

版本完成后的首选入口：

```powershell
.\release-current.ps1
```

该脚本以 `VERSION` 为唯一目标版本来源，自动规范 `release/vX.X.X`、补齐缺失 Release Record、生成 `scripts/releases/release-vX.X.X.ps1`、同步结构化版本声明，并调用 `publish.ps1` 进入 PR / validate / main / Pages。

发布自动化不会执行 Supabase SQL，不会 reset Database / Storage；migration 仍是明确的人工 Production 操作。
