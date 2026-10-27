# Prompt — Scene Runtime：防残影 / 防空窗 / 防错页闪现

这是 Starbook 所有页面切换的核心性能 Prompt。任何 Agent 修改 Scene Manager 前必须先读本文件。

## 核心问题
旧实现把 `swap()` 当成同步函数，但多个 scene 的 `enter()` 实际是 async。遮罩可能已经退场，目标首屏仍未准备，因此会出现：
- 上一页短暂残留；
- 只有背景等待内容；
- 多个 scene class/style 在异步过程中交错，出现错页闪现。

## 必须采用的事务
`prepare target → cover/transition → activate target → await enter → await nextPaint → reveal → cleanup`

## Scene Contract
- `prepare(params, opts)`：可选；加载网络资源、地图、Signed URL、Three.js 等，不依赖 scene 已可见。
- `enter(params, opts)`：允许返回 Promise；Scene Manager 必须 await。
- `leave(opts)`：停止 RAF/timer/audio，允许返回 Promise。
- `SB.scenes.prefetch(id, params)`：幂等预热，不改变当前 scene。

## 约束
- 任意时刻只允许一个普通 `.sb-scene.is-active`。
- Portal 可以临时给 target `is-entering`，但旧 scene 必须被稳定 backdrop 隔离。
- transition 结束必须清理 clip-path、ring、backdrop、busy class。
- popstate 只追最后一个 pending history target。
- 不允许用长 `setTimeout` 维持双 scene 共存。

## 验收
连续执行：`Login → Book → Globe → Country → City → Player → Back`，不得出现旧页残留、空背景等待、其他页面闪现。
