# Prompt — 地球 → 国家星门面板：地图预取与裂隙展开稳定性（v1.11.0 重写）

> v1.10.2 及以前这里是「地球 → 国家场景 Portal 转场」。v1.11.0 国家页改为地球上的悬浮面板（`prompts/09-country-map.md`），本文件随之更新。

## 目标
- 展开过程中地球不重建、不闪烁；面板内容在裂隙撕开前已经布局完成。
- 省级地图数据尽量在点击前就绪；没就绪时面板照常展开，地图区域显示小法阵，加载完成后描边浮现。
- 安卓 / 柔和档在展开、合拢期间保持稳定帧率。

## 必查文件
- `blocks/07-globe.html`（点击、update / prepare / enter / leave、渲染跳过）
- `blocks/09-country-map.html`（`SB.countryPortal`）
- `blocks/06-world-geo.html`（`loadCountryMap` 缓存）
- `blocks/00-core.html`（`update` 钩子）

## 正确链路
- 点击：`hover 180ms 预取 loadCountryMap → 轻点 → go('globe', {k}) → update → countryPortal.open → 布局面板（不可见）→ WAAPI 裂隙展开 → 地图绘制（若数据已就绪则在展开前绘制）`
- 返回 / 深链：`veil cover → globe.prepare（引擎 + 地图）→ swap → enter：静态呈现面板 → nextPaint → reveal`

## 实现要求
- 裂隙形状用 WAAPI `clip-path: inset()` 关键帧；边缘光线是两个独立元素，只动画 `transform / opacity`。
- 不对 WebGL 画布使用 CSS `filter`；变暗用幕布。
- 华丽档面板背景 canvas 约 30fps，仅面板打开时运行，像素比 ≤ 1.5；柔和档 / 安卓用 CSS 光带（transform 动画）。
- 地图描边绘入（`stroke-dashoffset`）只在华丽档；柔和档整体淡入。
- 柔和档 / 安卓：面板完全展开且飞转结束后，地球循环跳过渲染。
- 同一国家重复打开不重复下载地图脚本（`loadCountryMap` 缓存）。

## 验收
- 中国 / 美国 / 日本首次打开：裂隙展开流畅，地图在 1 秒内出现，无空白跳动。
- 安卓 UA 模拟：展开期间无长任务 > 100ms（地图数据已缓存时）。
