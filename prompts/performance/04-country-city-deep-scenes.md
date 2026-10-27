# Prompt — 国家 → 城市 → 回忆：深层页面首屏准备

只优化深层页面的首屏数据、媒体预取与场景比例，不改变现有 City Album / Player / Editor 视觉语言。

## 目标
- Country → City 时首屏章节封面在揭示前批量签名，不让卡片先空着再逐张跳出。
- City → Player 时先准备 cover 和前几张照片，再揭示放映厅。
- 打开 Memory Editor 时已有照片 Signed URL 提前批量预取，但弹窗不能等待全部照片加载完成。

## 必查文件
- `blocks/10-city-album.html`
- `blocks/11-memory-player.html`
- `blocks/12-memory-editor.html`
- `blocks/05-store.html`
- `blocks/00-core.html`

## 实现要求
- `city.prepare()` 只预取首屏需要的少量 cover，不签整座城市所有照片。
- `player.prepare()` 调用可 await 的 `prime(memory)`。
- `prime()` 批量 Signed URL，并只 decode 有限前几张。
- Editor 只后台预取现有照片 URL；离屏图片继续 lazy + async decode。

## 验收
- 手机进入有多段回忆的城市，首屏不连续闪现图片。
- 进入 Player 后封面和前几张照片明显更快。
- 20+ 张照片的 Editor 不因一次性 decode 全部照片而卡住。
