# Prompt — 地球 → 国家：地图数据预取与 Portal 稳定性

只优化性能与转场事务，不更改国家地图视觉设计。

## 目标
- 国家省级地图数据必须在目标场景揭示前准备完成。
- Portal 期间不能看到旧 Globe DOM 残留在新 Country 背后。
- 也不能切到只有国家页背景、随后省份轮廓才突然出现。

## 必查文件
- `blocks/07-globe.html`
- `blocks/01b-gate.html`（v1.8.0 幻影显形装饰；大洲目录页 `08-continent` 已删除）
- `blocks/09-country-map.html`
- `blocks/06-world-geo.html`
- `blocks/00-core.html`

## 正确链路
`hover/focus prefetch → click → prepare(country map) → portal backdrop → swap → draw → first paint → reveal`

## 实现要求
- Globe hover 后短延迟预取 `country`。
- 搜索结果信息卡「进入 X 地图」出现时预取该国家地图（v1.8.0；大洲目录卡片已删除）。
- `country.prepare()` 复用 `SB.geo.loadCountryMap()` cache。
- `country.enter()` 必须 return/await `load()`。
- Portal 外圈区域使用稳定 backdrop，不得露出旧 scene。

## 验收
- 中国/美国/日本等有省级地图的国家首次进入不出现空白等待。
- 快速重复进入同一国家不重复下载地图脚本。
