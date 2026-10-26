# 块 00 · 公共核心 提示词

## 设计令牌
- 书的世界：`--ink #0d0805`、`--leather #3a2416`、`--gold #f4b860`、`--gold-hi #ffe2a8`、`--gold-dim #9a6a2c`、`--ember #ff9a3c`
- 星图世界：`--night #070818`、`--night-2 #12153a`、`--aurora #8fa4ff`（只作冷色点缀）
- 文字：`--text #f6e7cc`、`--text-dim #bfa582`
- 浮层：`--glass rgba(24,14,8,.78)`、`--line rgba(244,184,96,.38)`
- 字体：`--f-title` ZCOOL XiaoWei、`--f-body` Noto Serif SC、`--f-rune` Cinzel Decorative

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
