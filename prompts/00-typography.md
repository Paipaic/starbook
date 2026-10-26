# 块 00-core · 「星文」字体系统 提示词（v1.5.2）

> 依据：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 3、4 节的实测与调研。
> 范围：Magic Celestial Theme 的字体、字号、字距、行高、数字与图标。只改表现层，不改任何数据与运行时链路。

## 1. 目标

1. 彻底消除“乱码”：不再出现实心方块、空心方框、Emoji 替身、同一行两种字形。
2. 全站只用一个中文超家族，标题有电影海报的庄重感，正文读起来舒适不累眼。
3. 拉丁铭文像《指环王》海报的罗马碑铭；数字像古典书籍里的数字，清楚可读。
4. 手机与电脑都流畅：字体按需加载，加载前后版式不跳动。

## 2. 字体家族（全部来自 Google Fonts，开源 OFL）

| 令牌 | 字体 | 用途 | 字重 |
|---|---|---|---|
| `--f-display` | Noto Serif SC（思源宋体） | 所有中文标题、按钮、标签 | 600；封面书名 900 |
| `--f-body` | Noto Serif SC | 正文、说明、输入框 | 400 |
| `--f-rune` | Cinzel | 只用于拉丁大写铭文（ORBIS STELLARUM 等） | 400 / 500 |
| `--f-num` | Cormorant Garamond | 数字、日期、计数、页码 | 500 / 600 |

- `--f-title` 保留为 `--f-display` 的别名，旧代码无需逐个改名。
- 每个字体栈都以 **Noto Serif SC** 作为中文后备：铭文或数字里夹着中文时（如「2026 年 5 月」「中国 · 四川」），中文仍由同一个思源宋体绘制，不会混入别的字形。
- 后备顺序：`Noto Serif SC → Source Han Serif SC → Noto Serif CJK SC → Songti SC → STSong → serif`。
- 彻底移除 **ZCOOL XiaoWei** 与 **Cinzel Decorative**。

## 3. 加载策略

- 一个 Google Fonts 链接加载：Noto Serif SC 400/600、Cinzel 400/500、Cormorant Garamond 500/600 与 500 斜体，`display=swap`。
- 封面书名的 900 字重只用到四个字，单独用 `text=星屿之书` 子集化加载，几 KB。
- 中文字体由 Google 按 unicode-range 切片，浏览器只下载页面实际用到的字。
- `SB.type.ready`：用 `document.fonts.load()` 预热关键字形，完成后给 `<html>` 加 `sb-fonts-ready` 类（只用于诊断，不隐藏文字，避免字体失败时页面空白）。

## 4. 字号阶梯（px，手机按 clamp 自动缩小）

| 令牌 | 值 | 用途 |
|---|---|---|
| `--fs-cap` | 12 | 角标、铭文小字 |
| `--fs-sm` | 13.5 | 次要说明 |
| `--fs-body` | 15.5 → 16 | 正文 |
| `--fs-lead` | 17 | 卡片标题、菜单项 |
| `--fs-h3` | 20 | 小节标题 |
| `--fs-h2` | clamp(22, 2.4vw, 28) | 区块标题 |
| `--fs-h1` | clamp(30, 5.2vw, 56) | 场景标题 |
| `--fs-hero` | clamp(38, 7vw, 72) | 城市名、放映标题 |

## 5. 行高与字距

- 正文行高 `1.8`（CJK 建议约 1.7，深色背景上略放宽）；标题 `1.25`；界面控件 `1.45`。
- 字距：大标题 `.2em`，场景标题 `.16em`，按钮/标签 `.08em`，正文 `.02em`，拉丁铭文 `.32em`。
- **居中的大字距标题**：末字后的字距会让整体视觉偏左，用与字距相同的 `padding-left` 补偿光学居中。
- 标题 `text-wrap: balance`，正文 `text-wrap: pretty`；`line-break: strict` 保证标点不在行首。
- 支持的浏览器启用 `text-autospace` 自动在中文与拉丁、数字之间加细空。

## 6. 渲染质量

- `-webkit-font-smoothing: antialiased`、`text-rendering: optimizeLegibility`、`font-kerning: normal`。
- `font-synthesis: none`：禁止浏览器伪造粗体/斜体（伪粗体是“糊字”的常见原因）。
- 数字统一 `font-variant-numeric: lining-nums`；统计数字再加 `tabular-nums`，滚动计数时不抖动。
- 标题金色：`.sb-foil` 类，金属渐变文字（亮金 → 琥珀 → 暗铜 → 亮金）+ `drop-shadow` 柔光（渐变文字不能用 text-shadow）。

## 7. 图标替换（`SB.icon(name)`）

把所有依赖系统字体的符号换成内联 SVG（`currentColor` 描边/填充，1em 大小，与文字基线对齐）：

| 原符号 | 图标名 | 位置 |
|---|---|---|
| ✦ | `spark` 四芒星 | 提示条、封面装饰、点亮反馈 |
| ★ | `star` 四芒星（实心） | 城市数徽章、封面标记、总览足迹 |
| ✎ | `quill` 羽毛笔 | 编辑城市 |
| ✕ × | `close` | 关闭、移除 |
| ⟲ | `reset` | 地图复位 |
| ＋ － | `plus` `minus` | 缩放、添加 |
| ↑ ↓ | `up` `down` | 照片排序 |
| › | `chevron` | 魔法路径分隔 |

- `SB.ui.button(text, kind, onClick, icon)`：新增可选的第四个参数，按钮前置图标，旧调用不受影响。
- 提示条左侧固定一个发光四芒星（CSS 遮罩绘制），调用处不再拼接符号。
- ♪ 和 ★ 这类思源宋体已包含的字符，在纯文字位置（菜单说明、编辑器标签）保留原样。

## 8. 封面 SVG 文字

- 书名「星屿之书」：Noto Serif SC 900，配合原有压印烫金滤镜。
- 「THE BOOK OF STAR ISLES」、环形铭文、「MMXXVI · LIBER PRIMUS」：Cinzel 500。
- 环形铭文和副标题里的 ✦ 改为 `·` 分隔与 SVG 绘制的小四芒星。

## 9. 验收

- 「回忆总览」「最近的回忆」「徘徊」等字正常显示，无实心方块。
- 页面中不再出现 `ZCOOL XiaoWei`、`Cinzel Decorative` 与 `✦ ✎ ✕ ⟲`（`tools/check_project.py` 增加回归检查）。
- 总览统计数字「1」是阿拉伯数字。
- 390px 手机宽度下，所有标题不溢出，按钮文字不换行错位。
