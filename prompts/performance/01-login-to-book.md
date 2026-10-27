# Prompt — 登录 → 魔法书：首帧一致性优化

你正在优化 Starbook 的「登录 → 魔法书」转场。只做性能与生命周期修复，不重做视觉设计。

## 目标
- 登录成功后绝不能先看到只有 Ambient 背景、随后魔法书再突然出现。
- Gate 淡出前必须保证：Auth 完成、Book Context 完成、`book_data.payload` 完成读取、`book` scene 已进入并完成至少一次 paint。
- 禁止在启动阶段为整本书所有照片 / BGM 一次性创建 Signed URL；媒体必须按进入 City / Player 时按需预取。
- 手机端登录卡片避免高成本实时 `backdrop-filter`。

## 必查文件
- `blocks/00-runtime.html`
- `blocks/05-store.html`
- `blocks/99-boot.html`
- `blocks/00-core.html`

## 正确链路
`Auth → Book → Store JSONB → scenes.boot(book) → nextPaint → hide Gate`

## 禁止
- 在 `finishAuthenticated()` 中直接隐藏 Gate。
- `SB.store.ready` 之前隐藏 Gate。
- Store 初始化时 `await` 全量媒体签名。
- 为了“看起来快”删除现有登录视觉。

## 验收
1. 冷启动登录后 Gate 退场时魔法书已经完整存在。
2. 已登录刷新同样无空背景窗口。
3. 数据量增加到上百张照片时，登录到书封面时间不随全部媒体数量线性增加。
