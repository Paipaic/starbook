# Starbook Performance Guide

> v1.7.3 起的性能与场景事务基线。新 Agent 修改场景、照片、放映、编辑器或视觉特效前必须遵守。

## 1. 场景切换

统一生命周期：

`prepare target → transition cover → activate → await enter → await nextPaint → reveal → cleanup`

- `prepare()` 用于网络 / Three.js / 地图 / Signed URL 等目标资源预热，不改变当前 scene。
- `enter()` 允许 async，Scene Manager 必须 await。
- 旧场景不得在目标场景揭示后继续保持 `is-active`。
- Portal 外圈必须由稳定 backdrop 隔离旧 scene，禁止把旧 DOM 当 portal 背景。
- Login Gate 只有在 Book 首帧完成后才能隐藏。
- 不允许 Store 启动全量签名全部媒体。
- 对应逐链路 Prompt：`prompts/performance/01-05`。

## 2. 性能档

`SB.perf.level`：

- `high`：桌面 / 较强设备。
- `low`：coarse pointer、小视口、低 CPU core 或低 device memory。
- `reduced`：系统 `prefers-reduced-motion`。

任何新增 Canvas / 粒子 / blur / backdrop-filter 动效都必须考虑 low / reduced。

## 3. 图片加载

- 城市目录：首屏封面可 eager；其余封面、缩影必须 lazy。
- 编辑器照片网格必须 lazy + async decode。
- 放映前使用 `SB.player.prime(memory)` / `SB.store.prefetchUrls(paths)` 预热前几张照片和 Signed URL。
- 放映过程中维持有限的前向预取窗口，避免一次请求全部大图。
- 不允许重新引入公开 `data/db.json` 或 GitHub runtime persistence。
- Private Storage 路径为唯一生成 ID，适合长期浏览器缓存；不要用原文件名覆盖同一路径。

## 4. Canvas / 粒子

- low / touch 设备降低 DPR 与粒子数量。
- 播放器正在放映时 Ambient FX 必须主动降帧，让主线程 / GPU 优先给照片变换和字幕。
- 不要在每一帧新增大量 DOM / Canvas 对象。
- 离开 scene 后必须停止对应 RAF / timer / audio。

## 5. 响应式比例

- PC 和手机不得仅靠整体缩放桌面布局。
- City Album：手机海报优先 3:2；极窄屏 4:3，减少竖图被 16:9 过度裁切。
- Memory Editor：桌面双列；手机单列；极窄屏照片卡片单列并扩大可编辑区域。
- Player：全幅镜头可保留 cinematic crop；framed / print / gilt 应尽量按照片原始 `w/h` 计算尺寸。
- 所有深层页面必须考虑 `100dvh`、safe-area 与触控目标。

## 6. 不以视觉换性能的原则

优先优化：
1. 下载数量 / 加载优先级；
2. DOM 是否离屏仍在布局；
3. Canvas DPR / FPS；
4. blur / backdrop-filter；
5. 动画时长与同时活动 scene 数量。

除非 Owner 明确要求，不要为了性能删除既有主题、季节、放映风格或核心视觉语言。

## 7. v1.7.3 验收

至少实测：
- 手机连续切换 Globe → Country → City → Player → Back，无上一页残影；
- City 有多段回忆时滚动不卡顿；
- 打开有多张照片的编辑器，不一次性加载所有离屏照片；
- 弱网 / 手机进入放映后前几张照片能提前加载，buffer 次数减少；
- PC 端 player 保持流畅；
- 手机横竖屏与 ≤430px 窄屏下编辑器、海报、照片卡片比例正常。

## 8. v1.8.0 新增视觉层的性能约束

- **秘境之门 `#sb-magic-gate`**：只在转场期间显示并运行 RAF，结束后清空画布并停止；DPR high ≤ 1.5、low = 1；low 档光丝 / 彗星数量减半、去掉宽光晕描边；reduced 档不显示（Scene Runtime 直接切换）。门钥匙的光幕一次绘制到半分辨率离屏画布，每帧只 `drawImage`。每个 cover / reveal 都有 `setTimeout` 兜底，后台标签页 RAF 暂停时事务也不会卡住。
- **魔法书烟雾 / 火星画布 `#bk-fxc`**：high 全量、low 0.45 倍、reduced 关闭；离开 Book 场景时清空粒子。3D 符文环 high 28 枚（带发光）、其余 16 枚无 drop-shadow。
- **地球新增层**：云雾纹理 high 768×384 / low 512×256，一次生成；星座线 / 足迹光点 low 减量；全部为静态几何，每帧只更新 uniform 与少量变换。
- **搜索**：离线库 648 城（约 30KB，随页面加载）；在线搜索只在输入停顿 350ms 后请求，`AbortController` 取消旧请求、6 秒超时、结果缓存。

## 9. v1.8.1 补充

- **曝光**：叠加（`lighter`）层 alpha ≤ 0.55；汇聚到一点的粒子随距离淡出；全屏遮罩只用深色。这既是视觉规则，也避免 GPU 在叠加大量高亮像素时掉帧。
- **新门**：墨金书页每帧只有 1 次裁剪 drawImage + 3 条描边 + 少量金尘；冥想盆为 1 次底色 drawImage / 遮罩 + ≤ 5 条涟漪 + ≤ 6 条丝缕。low 档去掉宽光晕描边、粒子减半。
- **时光长卷**：只在拖动 / 惯性 / 跳转时运行 RAF，静止时零开销；只对屏幕附近（±1.2 屏宽）的卡片计算景深；封面 lazy + 进入前预签最近 14 张；reduced 无惯性与视差。
- **工具标识**：面板只在打开时渲染；音柱动画为 3 根 CSS 变换，reduced 关闭。

## 10. v1.8.2 手机红线（iPhone 实测反馈）

- 开书 / 任何可见动画期间不要做 WebGL 初始化、着色器编译、大纹理生成；放到遮罩盖满之后或首次需要时。
- 3D `preserve-3d` 上下文里不要放与主体平面相交的移动元素（WebKit 平面切割 → 闪烁）。
- 手机档：不用 `mix-blend-mode`、大面积 `mask`、`feSpecularLighting`；不对带滤镜的 SVG 每帧改属性；按钮不用 `backdrop-filter`。
- 程序纹理结果缓存到 localStorage（带版本号键名）；只在首次访问生成。
- 验证方式：手机仿真 + 4× CPU 降速 + 长任务观测（`PerformanceObserver('longtask')`）+ CDP 采样，比较修改前后。

## 11. v1.9.2 放映流畅度
- 时钟循环：华丽档不设帧间隔下限（跟随 rAF）；柔和档 30fps 且允许 4ms 误差——不要再写 `now - last < 1000/60` 这种会在 60Hz 屏幕上随机丢帧的判断。
- 文字元素在进场完成、未开始退场时进入「定格」状态（`n.settled`），只更新整体位置 / 透明度，不再逐字写样式。
- 放映开始前预载前 12 张照片（最多 8 秒），其余顺序后台解码；`waitingAt()` 仍是最后的保护。
- 新画框（拱窗 / 卡纸 / 侧栏）只用 border-radius、box-shadow 与静态渐变遮层，不使用 mask；照片虚焦 / 压暗（rack）在柔和档只改亮度。

## 12. v1.10.0 时光之环 / 时光剪影
- 时光之环：自做透视投影；每帧只写卡片的 transform，透明度 / 层级 / 可点击状态只在变化时写入；环线按纵深分桶合并路径（每帧十几次描边）；柔和档 30fps、画布 dpr 1；静止档不自转、不摆动、不运行常驻循环；页面隐藏或离开场景时停止循环。
- 测量（手机仿真 4× CPU 降速）：静止 120ms/s（v1.9.2 直线时光轴 165ms/s）；拖动 433ms/s（直线时光轴 338ms/s）。
- 时光剪影：全部动画为 CSS 关键帧（transform / opacity），剪影 → 彩色用两层同图交叉淡化（剪影层的滤镜是静态的，不逐帧计算）；照片先预载。

## 13. v1.10.1 时光之环优化

- DOM 卡片数量有上限（电脑 ≤ 4 张、手机 ≤ 3 张 + 过渡中的 1–2 张），其余回忆是 canvas 光珠；不在窗口内的站点 `display:none`。
- 图片只为窗口 ±3 站预取签名并解码后淡入；不要用 `loading=lazy`。
- `sb:data` 先比对签名（回忆 / 城市 / 纪念日 / 日期），未变化只补图，不重建 DOM。
- 环线、延伸线文字、光珠、节点星环只在环转动 / 悬停变化时重画到离屏画布；静止时每帧只贴两张图 + 少量光晕（光晕用预渲染贴图，不再每帧新建径向渐变）。
- 实测（手机仿真 390×844，4× CPU 降速，32 段回忆）：拖动窗口主线程 562 ms/s（v1.10.0 为 695 ms/s）；静止时脚本 46 ms/s（v1.10.0 为 15 ms/s，多出的是笔尖与卡片偏转动画，柔和档 30fps）。

## 14. v1.10.2 安卓

见 `prompts/performance/06-android.md`。要点：大图在手机上先缩到显示尺寸（`SB.store.displayUrl`）；放映 low 档只用 transform（画内运动 = 放大的 img 在裁切框内平移，不改 `object-position`；框等比变化用 `scale()`）；安卓上不用 JS 逐帧改写遮罩 / 裁切；全屏 canvas 像素比 ≤ 1；不要在动画循环里写样式后立刻读布局（`offsetWidth` 等）。
