# Prompt — 魔法书 → 地球：WebGL 首帧准备优化

只优化转场性能和首帧准备，不改变魔法书开启动画、地球视觉主题或交互语义。

## 目标
- Flash 退场前，Three.js、renderer、地球纹理、几何体和首帧必须已准备。
- 不允许先切到 Globe 背景，再显示「正在描绘星图」或等待地球出现。
- Three.js 脚本可以在魔法书停留期间 idle 预热；WebGL 重初始化必须缓存。
- 手机降低初始化成本，但保持现有视觉语言。

## 必查文件
- `blocks/04-book-opening.html`
- `blocks/07-globe.html`
- `blocks/00-core.html`
- `blocks/99-boot.html`

## 正确链路
`Book opening → flash cover → globe.prepare() → globe.enter() → first paint → flash reveal`

## 性能原则
- low/touch：降低 Sphere segment、Canvas texture resolution、粒子数量、antialias 成本。
- `init()` 必须幂等；已经 ready 时立即返回。
- Scene Manager 必须 `await enter()`。

## 验收
- 手机首次打开地球时不出现空背景等地球。
- 第二次进入 Globe 基本即时。
- 魔法书动画结束与地球出现之间没有页面闪烁。

## v1.8.2 修订（Owner 真机反馈：开书动画完全看不见，卡几秒直接跳到星图）
- 实测（手机仿真 4× CPU）：开书第 1.4 秒调用的 `SB.scenes.prefetch('globe')` 会同步创建 WebGL 上下文并编译着色器，主线程被占用数秒，开书动画全部冻结。
- 规则：**开书动画期间不得创建 WebGL / 编译着色器**。`04-book-opening` 不再调用 `prefetch('globe')`；Three.js 脚本仍在魔法书停留时 idle 下载（`warmEngine`，只是网络与解析），WebGL 初始化在门钥匙**盖满画面后**的 `prepareTarget` 中进行（此时画面静止也不会被看见）。
