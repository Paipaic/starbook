# Starbook 视觉升级计划（v1.5.2 → v1.6.2）

> 本文是 Magic Celestial Theme 视觉升级的总计划、调研记录与版本拆分依据。
> 它只覆盖**视觉 / 表现层**：不修改 `SB.user / SB.book / SB.store`、Supabase schema、RLS、Storage、CI 发布链路。
> 每个版本开发时：先读本文对应章节 → 写/更新 `prompts/` 下的提示词 → 再改代码 → 同步版本治理文件。

## 1. 用户需求（2026-10-26 Owner 提出）

1. 字体：部分文字显示像乱码，需要一套完整、流畅、阅读舒适的字体系统。
2. 魔法书页面、地球页面的视觉特效更丰富，有层次感和高级感。
3. 页面跳转、转场画面重新设计，全部围绕「奇幻」主题。
4. 照片放映不要死板：像放电影一样逐张呈现，照片出现/消失的细节要设计；增加「放映」按钮，自动播放照片和文字。
5. 第 2、3 点参考《指环王》《哈利·波特》等奇幻电影的视觉效果，精致、高级、流畅、自然、有设计感。

## 2. 版本拆分

| 版本 | 主题 | 主要涉及块 | 风险 |
|---|---|---|---|
| **v1.5.2** | 「星文」字体系统：修复乱码，统一中文 / 拉丁 / 数字 / 图标 | 00-core 及各场景的字体与符号 | 低 |
| v1.6.0 | 「冥想盆放映厅」电影式回忆放映 + 放映按钮（新增用户能力 → 次版本号） | 11-memory-player、10-city-album | 中 |
| v1.6.1 | 「秘境之门」奇幻转场系统 | 00-core（转场层）、01-ambient-fx、04-book-opening | 中 |
| v1.6.2 | 「星辉层次」魔法书与地球特效 | 03-magic-book、07-globe、01-ambient-fx | 中 |

拆分原则：
- 每版只动一类视觉，便于在 Production 上单独验证与回滚；
- 版本号按**交付顺序**递增（语义化版本不能回退）。放映排在第二：它是周年当天最常被观看的部分，若 2026-10-28 晚 Feature Freeze 前时间不足，转场与特效可顺延到周年之后。
- Owner 原始需求编号与版本对应：需求 1 → v1.5.2，需求 4 → v1.6.0，需求 3 → v1.6.1，需求 2 → v1.6.2。

## 3. v1.5.2 调研：乱码根因（实测）

在本地用真实字体文件（Google Fonts 仓库）+ Chromium 渲染 v1.5.1 后确认：

1. **ZCOOL XiaoWei 自身字形损坏**：`回 圃 圄 圊 崮 徊` 在 Chromium 和 FreeType 下都渲染成实心方块（内外轮廓同向，被整块填充）。
   本项目大量使用「回忆」，因此「回忆总览」显示为「■忆总览」，这是用户看到的“乱码”主因。
2. **ZCOOL XiaoWei 只覆盖约 7000 字（GB2312）**：用户输入的城市名、照片描述中稍罕见的字（如日本地名「埼玉 / 栃木 / 新潟」）会回退到其他字体，同一行出现两种字形。
3. **符号字形缺失**：`✦ ✎ ✕ ⟲` 在项目所有网页字体中都不存在，手机会回退成系统 Emoji 或空心方框。
4. **Cinzel Decorative 不适合数字和小字**：数字 `1` 显示为罗马式 `I`（总览统计「1」看起来像字母），小字号下花体大写难以辨认。
5. Windows 等系统的回退字体为宋体位图风格（SimSun），网页字体加载前后差异大。

## 4. v1.5.2 调研：字体选择依据

- CJK 正文行高建议约 **1.7**（Typotheque《Typesetting principles of CJK text》），中文无连字符断行、避免行首标点。
- 《指环王》系列海报标语使用 **Trajan Pro**（罗马碑铭大写）与 **Kennerley 小型大写**，DVD 菜单使用书法体（TheOneRing.net 字体指南）。开源的 **Cinzel** 正是以罗马碑铭大写为蓝本设计，适合拉丁铭文；同指南提到 **Garamond Premier Pro** 用于仿片尾字幕，对应开源 **Cormorant Garamond**。
- 中文电影海报（含《哈利·波特》《指环王》中文版）普遍使用**宋体 / 明朝体**展示标题。思源宋体（Noto Serif SC）覆盖 3 万+ 字形（含全部 GB18030 常用汉字），多字重，本地实测无损坏字形。

结论：**一个中文超家族（Noto Serif SC）+ 一款拉丁碑铭体（Cinzel）+ 一款古典数字/拉丁正文体（Cormorant Garamond）+ 一套内联 SVG 图标**。

## 5. v1.6.0 / v1.6.1 / v1.6.2 调研摘要（供后续版本使用）

奇幻视觉语言（摘自 fxguide 对 Double Negative《哈利·波特》特效的访谈、TheOneRing.net 对 Animal Logic 真知晶球的报道等）：

- **光是有来源的**：Patronus 的光会照亮周围；烟火的每个粒子都是光源 → 转场光要从具体位置（宝石、点击点、星星）发出，并照亮画面。
- **旋转螺旋 + 细丝**：凤凰社幻影显形是「明亮蒸汽的螺旋涡流 + 极细的丝线」 → 转场使用螺旋光丝而不是纯色遮罩。
- **力量的不稳定感**：咒语周围有轻微湍流扭曲 → 关键动作配轻微的画面扭曲/波纹。
- **多层叠加的深度**：真知晶球 = 多层云雾 + 火花纹理 + 反射环境色，表面持续“活着” → 地球/宝石要多层、持续缓动。
- **冥想盆（Pensieve）回忆**：墨滴入水的转场 + 像隔着水的有机波动（倾斜 skew + 轻微旋转 + 少量缩放，不依赖泛光） → 放映入场使用“墨滴扩散 → 回忆浮现”。
- **溶解**：画面被柔化、调色、逐渐混合消失，暗示进入灵界 → 照片退场使用柔化 + 金色光尘溶解。

电影式放映（Ken Burns、婚礼高光剪辑、光漏用法）：

- Ken Burns：缓慢推拉与平移引导视线，模拟视差把平面照片变成纵深空间，用淡入淡出连接镜头。
- 情感剪辑：只用最好的素材、开场给出主题、交叉溶解与硬切结合；**光漏要克制**，放在场景开始/结束或情绪高点，颜色与画面光一致，运动要轻。
- 字幕：电影式下方居中、逐字/逐行柔和出现，留足阅读时间。

## 6. v1.6.0 调研：电影式放映的具体参数

- **字幕**（Netflix 简体中文字幕规范）：成人节目阅读速度上限 9 字/秒；每行最多 16 个汉字；最多两行，两行时上短下长（金字塔形）；字幕不应遮挡画面关键内容，连续字幕保持同一位置。→ 本项目抒情字幕采用 7 字/秒、单条最短 1.8 秒，按标点切分长描述。
- **溶解**（Wikipedia: Dissolve）：溶解与淡入淡出通常 1–2 秒（24–48 帧），表达时间流逝或进入闪回；6–12 帧的短溶解用于柔化硬切。→ 自动放映 1.6 秒，手动翻页 0.8 秒。
- **Ken Burns**（PTE AV Studio 文档）：线性关键帧会显得生硬，应改为平滑曲线；深度放大需要足够分辨率（放大 2 倍需要 2 倍像素）。→ 本项目使用正弦缓动，放大上限 1.12（照片长边 2400px）。
- **静态照片成片**（No Film School / Vashi Nedomansky）：每一张静帧都要在它的时刻成立，一张放错的照片会破坏节奏；剪辑理论（库里肖夫效应）同样适用于静帧蒙太奇。→ 保持用户排定的顺序，镜头语言按照片比例选择，转场以溶解为主。
- **光漏**（MotionElements）：少即是多；放在场景开始/结束或情绪高点；颜色与画面光一致；运动要轻。→ 每 4 个镜头最多一次，并用于最后一个镜头前。
- **冥想盆**（sinema.sg）：墨滴入水作为进入回忆的转场；回忆画面像隔着水，有机流动。→ 开场「墨滴入水」涟漪与第一张照片的墨渍揭幕。

## 7. 参考来源

- Typotheque — Typesetting principles of CJK text: https://www.typotheque.com/articles/typesetting-cjk-text
- TheOneRing.net — The Lord of the Fonts: https://www.theonering.net/torwp/2014/06/26/90498-the-lord-of-the-fonts-a-guide-to-fonts-in-the-hobbit-and-the-lord-of-the-rings/3/
- fxguide — Harry Potter: The Magic of Double Negative: https://www.fxguide.com/?p=21584
- TheOneRing.net — The Palantír before the Animal Logic magic touch: https://www.theonering.net/torwp/2002/07/25/26469-the-palantr-before-the-animal-logic-magic-touch-2/
- sinema.sg — Harry Potter inspired flashback (Pensieve): https://sinema.sg/2019/01/11/classroom-how-to-create-a-harry-potter-inspired-flashback-in-after-effects
- Wikipedia — Ken Burns effect: https://en.wikipedia.org/wiki/Ken_Burns_effect
- PremiumBeat — 5 tips for editing cinematic wedding highlight videos: https://www.premiumbeat.com/blog/5-tips-editing-cinematic-wedding-highlight-videos
- MotionElements — Mastering light leaks: https://www.motionelements.com/blog/articles/mastering-light-leaks-adding-cinematic-magic-to-your-videos
- Netflix — Simplified Chinese (PRC) Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215986007-Chinese-Simplified-Timed-Text-Style-Guide
- Wikipedia — Dissolve (filmmaking): https://en.wikipedia.org/wiki/Dissolve_(filmmaking)
- PTE AV Studio — Ken Burns Effect: https://docs.pteavstudio.com/en-us/9.0/techniques/kenburns
- No Film School — Making films with still images: https://nofilmschool.com/2013/12/if-youre-making-films-with-still-images-here-are-a-few-things-to-consider
