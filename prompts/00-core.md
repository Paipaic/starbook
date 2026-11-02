# 块 00 · 公共核心 提示词

## 设计令牌
- 书的世界：`--ink #0d0805`、`--leather #3a2416`、`--gold #f4b860`、`--gold-hi #ffe2a8`、`--gold-dim #9a6a2c`、`--ember #ff9a3c`
- 星图世界：`--night #070818`、`--night-2 #12153a`、`--aurora #8fa4ff`（只作冷色点缀）
- 文字：`--text #f6e7cc`、`--text-dim #bfa582`
- 浮层：`--glass rgba(24,14,8,.78)`、`--line rgba(244,184,96,.38)`
- 字体（v1.5.2 起）：见 `prompts/00-typography.md`「星文」字体系统 —— `--f-display`/`--f-body` 思源宋体（Noto Serif SC），`--f-rune` Cinzel，`--f-num` Cormorant Garamond；`--f-title` 为 `--f-display` 别名。图标用 `SB.icon(name)`，不再依赖系统符号字体。

## 全局背景层
- 固定铺满的暖光渐变 + 暗角；切到星图世界（地球、大洲、地图、相册）时平滑过渡为靛蓝夜空色调。
- 三团缓慢漂移的雾霭。
- 粒子画布分前景、背景两层（由块 01 绘制）。

## 场景管理器 `SB.scenes`
- `register(id, {enter(params), leave(), title(params)})`；`go(id, params, {transition})`。
- 维护历史栈：`back()` 回到上一场景（带参数）；`path()` 返回魔法路径。
- 转场：
  - `veil`：光尘向中心汇聚成金色光幕 → 切换 → 光幕向外散开（约 1.4 秒）。
  - `flash`：中心爆出暖白金光覆盖全屏 → 切换 → 淡出（约 1.6 秒）。
  - `portal`：一个发光圆环从点击处扩张，圆内是新场景（clip-path 圆形展开，约 1.1 秒）。
- 转场期间屏蔽点击；`#book`、`#globe` 锚点可直达。

## 通用界面组件 `SB.ui`
- `toast(text)`：底部金边提示。
- `dialog({title, body(el), actions})`：居中的魔法卷轴弹窗（玻璃深褐底、金色双线框、四角烫金角花），
  弹出时从中心缩放 + 模糊变清晰；手机上贴底展开成抽屉。按 Esc / 点遮罩关闭。
- `confirm(text)`：页面内确认框（不用浏览器自带弹框）。
- `field(label, input)`：表单行；输入框统一为深底金色下划线风格，聚焦时下划线发光。
- `button(text, kind)`：主按钮（金色渐变、光晕）、次按钮（金边透明）、危险按钮（暗红边）。
- `spinner(text)`：旋转的小法阵 + 文字，用于加载中。

## 工具
- `SB.perf`：`high / low / reduced` 三档。
- `SB.loadScript(urls[])`：按顺序尝试多个地址加载脚本，第一个成功即返回（用于地图数据和 3D 引擎）。
- `SB.esc(text)`：转义 HTML。

## v1.10.2 · 全局拖放保护与安卓识别
- `dragstart`（捕获阶段）：目标不在 `[draggable="true"]` 内时 `preventDefault()`——页面里没有需要原生拖拽的图片 / 文字；编辑器照片卡自己设置了 `draggable="true"`，不受影响；从桌面把文件拖进编辑器是 `drop` 事件，也不受影响。
- `SB.dragSurface(el)`：给拖动面用的小工具——按下时清除文字选区。
- `SB.perf.android`：UA 含 Android（安卓 Chrome / WebView）。用于少数安卓专属降级（见 `prompts/performance/06-android.md`）；不改变三档 `high / low / reduced` 的含义。

## v1.11.0 · 同场景状态钩子 `update(params, opts)`（国家星门面板）
- 背景：国家地图页改为世界星图上的悬浮面板（`prompts/09-country-map.md`）。面板需要进入浏览器历史（手机系统返回键先关面板），但不应触发全屏转场或重建地球。
- 规则：`SB.scenes.go(id, params, opts)` 的目标就是**当前场景**、且该场景注册了 `update(params, opts)` 时，先调用 `update`：
  - 返回 `false` → 按原流程走（转场 → prepare → swap）；
  - 否则视为已就地处理：更新 `scenes.params`，按原规则写历史（`fromHistory` 不写、`replaceHistory` 替换、其余 push），派发 `sb:scene`，不进入 `is-busy`、不走遮罩。
- 只用于「同一场景里的子状态」（例如面板开 / 关、切换国家）；需要准备数据或换场景时必须仍走 `prepare → await enter → nextPaint → reveal`。
- `update` 必须是同步的轻量操作（可以启动动画，但不能 await 网络）；动画中重复调用要能安全合并。
- `popstate` 仍调用 `go(..., {fromHistory:true, force:true})`；同场景时同样先走 `update`。
- `is-busy` 期间到达的同场景请求与以前一样排队到 `_pendingHistory`。
