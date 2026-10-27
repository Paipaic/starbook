# Starbook v1.7.3 Transition Stability Test

## 目的

专门验证 v1.7.3 修复的三类问题：

1. 前一页视觉残留；
2. 下一页只剩背景、内容晚到；
3. 转场期间其他 scene / block 突然闪现。

## A. 登录 → 魔法书

### 冷启动
1. 清理该站点登录状态或使用未登录浏览器。
2. 打开 Production。
3. 登录。
4. 观察 Gate 退场全过程。

### PASS
- Gate 淡出时魔法书已完整存在；
- 无纯 Ambient 背景空窗；
- 无 Globe / Country / City 等其他 scene 闪现；
- 回忆照片数量增加不会让登录阶段全量等待 Signed URL。

## B. 魔法书 → 地球

1. 登录停在魔法书。
2. 点击宝石。
3. 连续测试 3 次（返回 Book 后再进入）。

### PASS
- Flash 退场时地球已经可见；
- 首次进入不出现「只有夜空背景，地球稍后出现」；
- 第二次进入明显更快；
- 手机不出现长时间冻结。

## C. Globe → Country

优先测试：中国、美国、日本。

### PASS
- 点击后立即有 Portal 光环响应；
- 地图准备阶段 Globe 保持完整，不出现半页残留；
- Portal 展开时国家省级轮廓已经完成；
- 不出现 Country 背景先出现、轮廓后补。

## D. Country → City

选择至少有 3 段 Memory 的城市。

### PASS
- City 首屏卡片结构一次出现；
- 首屏 Cover 不连续从空白逐张突然跳出；
- 未进入视口的缩影继续 lazy load。

## E. City → Player

选择 8 张以上照片的 Memory。

### PASS
- 点击后 Portal 有即时反馈；
- 放映厅出现时 Cover 已准备；
- 前 1–2 张照片已预热；
- 不要求转场前下载全部照片。

## F. 快速返回 / 系统返回

连续执行：

`Book → Globe → Country → City → Player → Back → Back → Forward`

### PASS
- 任意时刻只有一个普通 scene active；
- 无其他页面闪现；
- URL / history state 与画面一致；
- 无永久 `is-busy`、veil、flash、portal backdrop 残留。

## 推荐设备

- iPhone Safari / 微信或系统内置浏览器可作为辅助；
- Android Chrome；
- Windows Chrome/Edge；
- 手机弱网可用 DevTools Fast 3G 进行额外测试。
