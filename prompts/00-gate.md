# 块 01b · 「秘境之门」奇幻转场 提示词（v1.8.0）

> 依据：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 5 节与 8.2 / 8.3 节（Double Negative 幻影显形 / 门钥匙、熄灯器、Animal Logic 真知晶球）。
> 必须遵守 `prompts/performance/05-scene-runtime-transaction.md` 与 `docs/PERFORMANCE_GUIDE.md`：不改变 `prepare → cover → activate → await enter → nextPaint → reveal → cleanup` 事务，只替换 cover / reveal 的视觉。

## 1. 设计原则（来自资料）
- **光有来源**：每种门的光都从一个具体的点（点击处、宝石、画面中心）发出，并照亮周围。
- **螺旋 + 细丝**：用旋转的光丝与蒸汽，而不是纯色遮罩（凤凰社幻影显形「闪亮蒸汽的旋涡 + 蛛丝般的细丝」）。
- **环境溶解、新地点成形**：门钥匙让旧画面旋入旋涡，新场景从中心向外「长出来」，有一点失去方向的感觉，但不晕眩。
- **有机、古老、克制**：不做霓虹、不做硬几何闪烁；金色、琥珀、暖白为主，夜色用深靛蓝。

## 2. 结构
- 新块 `blocks/01b-gate.html`：一个全屏画布 `#sb-magic-gate`（z-index 高于场景、低于菜单），只在转场期间显示和绘制；结束后清空并停止 RAF。
- 对外接口 `SB.gate`：
  - `cover(kind, {x, y})` → Promise：遮盖动画结束（画面已完全被门遮住）时 resolve；
  - `reveal(kind, {x, y})` → Promise：揭示动画结束时 resolve，并清理；
  - `portalStart(x, y)` / `portalFrame(x, y, r, k)` / `portalEnd()`：给 Scene Runtime 的圆形揭示加装饰；
  - `abort()`：异常时立即清理。
- `00-core` 的 `scenes.go`：`flash` 分支改用 `SB.gate.cover('portkey') / reveal('portkey')`，`veil` 分支改用 `'nox'`，`portal` 分支在已有 clip-path 圆形揭示的每帧调用 `portalFrame`；`SB.gate` 不存在时回退到旧的 veil / flash，保证不会卡住。

## 3. 三种门

### 门钥匙 Portkey（`flash`：魔法书 → 地球、菜单 → 地球）
- cover（high 620ms / low 420ms）：
  - 屏幕四周出现 40–70 条金色光丝（细贝塞尔弧），沿对数螺线向中心旋入，越近越快、越亮；
  - 中间叠加旋转的暖白蒸汽团（大而虚的径向渐变），整体顺时针旋转；
  - 中心光门（暖白 → 金 → 琥珀）从小迅速扩大到盖满全屏。
- reveal（high 760ms / low 520ms）：
  - 全屏光幕从中心挖开一个不断扩大的洞（羽化边缘 + 6–8 个随机偏移的小圆让边缘不规则，像光门撕开），新场景从中心向外显现；
  - 残余光丝反向向外甩出并淡出；
  - 起点：魔法书开书时用书页中心。

### 幻影显形 Apparition（`portal`：点击处圆形揭示）
- 准备阶段（等待 prepare 时）：点击处一个小的旋转符文环在呼吸（取代原来的纯光圈）。
- 揭示时，圆形边缘：
  - 一圈旋转的符文刻度环（双圈 + 刻度 + 四个菱形），跟随半径扩大，逐渐变淡；
  - 6 条螺旋金丝绕着边缘旋转；
  - 边缘外侧一圈柔光（照亮周围），向外抛出少量火星。

### 熄灯器 Deluminator / 荧光闪烁（`veil`：返回与菜单跳转）
- cover（high 520ms / low 360ms）：四周 30–60 颗光点像彗星一样拖着尾巴被吸向中心（各自弧线路径），同时深靛蓝夜色从四周向中心收拢，最后中心只剩一点光，然后熄灭（全屏夜色）。
- reveal（high 620ms / low 420ms）：中心先「荧光闪烁」亮起一点暖白光，光向外推开夜色（羽化的扩张洞），彗星光点向外散开淡出。

## 4. 性能与无障碍
- 画布 DPR：high ≤ 1.5，low 1；粒子数 low 减半；每帧只用 `drawImage` 精灵与少量 path，复合模式 `lighter`。
- reduced：Scene Runtime 已直接切换，不显示门。
- 门画布 `pointer-events:none`、`aria-hidden`；转场期间 `body.is-busy` 已阻止交互。
- 任何异常（目标场景准备失败）都必须 `abort()` 清理，不能留下遮罩。
