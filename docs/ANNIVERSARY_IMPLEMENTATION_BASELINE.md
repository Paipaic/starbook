# Anniversary Implementation Baseline

## 交付原则

原始桥接目标为 `v1.5.0-anniversary`；当前在同一周年交付主线上迭代到 **`v1.5.1`**。交付原则不变。

优先级顺序：
1. 能打开
2. 不丢数据
3. 私密
4. 手机可用
5. 原魔法书/地图/回忆体验不退化
6. 才考虑周年献词、结尾和彩蛋

## 现在保留的 V1
- blocks + build.py
- Magic Celestial 视觉
- World Map 场景
- City/Memory 数据对象
- Editor / Player / Overview 业务 API

## 现在改变的边界
- GitHub PAT → Supabase Auth
- db.json → book_data.payload JSONB
- media/ → Private Storage
- 唯一隐式 Book → `SB.book.current`
- 情侣/魔法书/地图从“系统唯一设定”变成当前 preset/context

## 截止日前禁止
- 多 Book UI
- 公众注册
- 多 Theme 真正实现
- Experience 插件系统
- 数据全面正规化
- Realtime
- PWA
- React/Vue/Vite 重构
- 大规模新特效

## 10/28 晚 Feature Freeze
之后只允许 Bug Fix、文案、数据和必要 UI 修复。
