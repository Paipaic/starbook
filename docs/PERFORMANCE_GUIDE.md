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
