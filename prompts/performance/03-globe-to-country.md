# Prompt — 地球 → 国家：地图数据预取与 Portal 稳定性

只优化性能与转场事务，不更改国家地图视觉设计。

## 目标
- 国家省级地图数据必须在目标场景揭示前准备完成。
- Portal 期间不能看到旧 Globe DOM 残留在新 Country 背后。
- 也不能切到只有国家页背景、随后省份轮廓才突然出现。

## 必查文件
- `blocks/07-globe.html`
- `blocks/08-continent.html`
- `blocks/09-country-map.html`
- `blocks/06-world-geo.html`
- `blocks/00-core.html`

## 正确链路
`hover/focus prefetch → click → prepare(country map) → portal backdrop → swap → draw → first paint → reveal`

## 实现要求
- Globe hover 后短延迟预取 `country`。
- Continent card pointerenter / focusin 预取。
- `country.prepare()` 复用 `SB.geo.loadCountryMap()` cache。
- `country.enter()` 必须 return/await `load()`。
- Portal 外圈区域使用稳定 backdrop，不得露出旧 scene。

## 验收
- 中国/美国/日本等有省级地图的国家首次进入不出现空白等待。
- 快速重复进入同一国家不重复下载地图脚本。
