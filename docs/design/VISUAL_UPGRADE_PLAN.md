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
| **v1.7.0** | 「光影放映」多图编排放映引擎 + 三种放映风格（银幕 / 星图 / 手札）+ 编辑器风格选择（新增用户能力 → 次版本号） | 11-memory-player、12-memory-editor | 中 |
| **v1.7.1** | 城市回忆目录页「星屿手稿 · 目录页」升级（Owner 追加） | 10-city-album | 低 |
| v1.7.2 | 「秘境之门」奇幻转场系统 | 00-core（转场层）、01-ambient-fx、04-book-opening | 中 |
| v1.7.3 | 「星辉层次」魔法书与地球特效 | 03-magic-book、07-globe、01-ambient-fx | 中 |

拆分原则：
- 每版只动一类视觉，便于在 Production 上单独验证与回滚；
- 版本号按**交付顺序**递增（语义化版本不能回退）。放映排在第二：它是周年当天最常被观看的部分，若 2026-10-28 晚 Feature Freeze 前时间不足，转场与特效可顺延到周年之后。
- Owner 原始需求编号与版本对应：需求 1 → v1.5.2，需求 4 → v1.6.0 / v1.7.0（Owner 2026-10-26 反馈后重做），需求 3 → v1.7.2，需求 2 → v1.7.3；城市目录页追加优化 → v1.7.1。

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

## 7. v1.7.0 调研：多图编排放映与放映风格

### 7.1 Owner 对 v1.6.0 的反馈（2026-10-26）

1. 不要拘束于「一页一张照片」：一个画面里可以同时有几张照片，部分渐渐消失，再渐渐出现新的。
2. 每张照片间隔偏长；版式太固定。
3. 字幕出现方式没有设计感、字太小、显得简陋。
4. 转换形式要多样，但衔接必须自然流畅。
5. 设置多种放映风格（初版 2–3 种），在添加 / 编辑回忆时用按钮选择；一定保证质量。

### 7.2 资料与结论

| 来源 | 要点 | 对本项目的结论 |
|---|---|---|
| Apple 照片「回忆」（iOS 10 / 15，AppleInsider、Photofocus） | 自动生成回忆影片；切换配乐会**整体重新剪辑**节奏与氛围；iOS 15 起有动画标题卡、多图拼贴标题卡、按节拍播放、「回忆外观」统一调色 | 「风格」不只是换转场，而是**一整套导演规则**（版式、节奏、转场、字幕、底色）同时改变 |
| Krumzi 幻灯片指南 | 每张 **3–5 秒**最舒服；更快显得慌乱，更慢显得拖沓；转场保持一两种一致的主转场；开场抓人、结尾落在情绪画面 | 单张焦点时间从 v1.6.0 的 5.2–16 秒压到 **约 3.2–3.6 秒**；只有字幕需要时才延长 |
| Pic-Time 摄影师幻灯片技巧 | 用**变化的版式**代替一张一张放；双图版式里**一张保持不动、另一张替换**；近景与远景交替，给观众喘息 | 采用「接力」：画面里的照片**不同时换**，总有一张留着，另一张渐隐、新的一张渐显 |
| 电影感照片（IT 之家 / 玩点摄影） | 2.39:1 宽画幅 + 底部字幕；**多帧拼接**讲故事，拼接的照片比例、色调要一致；暗角 | 「银幕」风格：宽银幕黑边 + 分屏拼接（双联 / 三联竖条），面板尺寸统一 |
| Saul Bass 片头（BFI 十部片头） | 《惊魂记》**竖条**错位滑入；《金臂人》线条汇聚成形；《纯真年代》蕾丝般半透明层层绽放；平面化、几何化 | 转场库加入「竖条错位」「光缝开合」「百叶」「虹膜」等几何遮罩转场，但放慢、柔和，适合抒情 |
| 王家卫《花样年华》（MovieMaker） | 画中画：画面里再套一层框；固定机位的重复让情绪变化更明显；时间跳跃 | 分屏 / 相框本身就是「画中画」；竖排大字幕呼应港片海报 |
| MinaLima《哈利·波特》平面设计 | 「把现实拿来，只偏移几度」；不用矢量死字而保留手工的细微不规则；按「谁写的」设计笔迹 | 「手札」风格：真实的相纸、桌面、烛光，文字像墨水写上去（逐字擦出 + 微小倾斜不规则），只偏移几度到魔法世界 |
| Motion Array 2.5D 视差 | 小而缓的运动最好；近处层比远处层移动更多；过多运动元素、夸张位移显得廉价 | 「星图」风格：卡片分前后景，**近大远小、近快远慢**的视差漂移，幅度 ≤ 2% |
| 运动字体（Resistenza Motion fonts） | 一次只动一个属性并保持克制；缓动避免机械感；不要用过细 / 过紧的字体做动画 | 每种风格只选**一种**字幕动画语言；字号大幅提升；中文继续用思源宋体 600 / 400 |
| Kinetic typography（Wikipedia） | 文字在 2D / 3D 空间相对运动（动态版式）；「流体文字」：字形本身变化（如《守夜人》字幕像血在水中化开） | 「手札」墨迹逐字显影；「银幕」字距收拢 + 去模糊；「星图」逐行遮罩上浮 |
| W3C《中文排版需求》clreq | 直排：字从上到下、行从右到左；大陆标点在直排中置于右上；直排多用直角引号 | 短句（≤ 12 字）在「银幕」宽屏全幅镜头中使用**竖排大字**，标点去尾 |
| Aquasoft 宝丽来、Swiper 宝丽来卡片模板 | 相片叠放、飞落到打开的日记上，逐张落下 | 「手札」：相片逐张落到桌面上堆叠，镜头随最新一张移动，旧照片自然移出画面 |

### 7.3 候选风格对比

| 候选 | 画面 | 优点 | 风险 | 结论 |
|---|---|---|---|---|
| 银幕 · 电影蒙太奇 | 宽银幕全幅 + 双联 / 三联分屏 + 几何遮罩转场 + 大字幕 | 最「像电影」，与 v1.6.0 的开场 / 终章一脉相承 | 转场太多会花 | **采用**（默认风格），每种转场只在适合的照片组合上出现 |
| 星图 · 星河拼贴 | 深夜星空里 2–3 张烫金相框照片前后漂浮，金线连成星座，接力更替 | 最符合「星屿 · 奇幻」主题；同屏多图 | 同屏三张时字幕空间紧张 | **采用**，每种版式预留文字区 |
| 手札 · 魔法手札 | 烛光书桌上相片逐张落下堆叠，墨迹手写旁白，镜头沿桌面移动 | 温暖、有触感，文字成为画面一部分 | 桌面质感做不好会廉价 | **采用**，桌面只用暗色皮革 + 烛光，不做卡通道具 |
| 冥想盆漩涡 | 照片绕中心旋转汇入 | 奇幻 | 旋转易晕、照片难看清 | 不采用（只保留墨滴开场） |
| 3D 照片墙穿梭 | 镜头在照片墙中飞行 | 炫 | 手机性能差、像模板 | 不采用 |
| 胶片条滚动 | 胶片条横向滚动 | 复古 | 照片很小、字幕位置差 | 不采用 |

### 7.4 关键参数

- 单张焦点时间：银幕 3.4s、星图 3.2s、手札 3.6s；有字幕时 = max(基础, 字幕阅读时间 + 0.6s)。
- 字幕阅读：每秒 7 字，单条最短 2s；一张照片的描述按标点切成若干条依次出现。
- 同屏照片数：银幕 1–3（分屏）、星图 2–3、手札 2–4（旧照片随镜头移出）。
- 转场时长：0.9–1.4s；接力替换时旧照片先开始消失，新照片在其后 0.3–0.6s 出现，永远不会出现「全部消失 → 空屏 → 全部出现」。
- 运动幅度：镜头推拉 ≤ 1.08；视差漂移 ≤ 2%；旋转 ≤ 8°（手札相片落下）。
- 字号：银幕字幕 clamp(24px, 3.4vw, 44px)，竖排 clamp(30px, 4.4vw, 56px)；星图 clamp(22px, 2.8vw, 38px)；手札 clamp(24px, 3.2vw, 42px)。

### 7.5 Owner 追加需求（2026-10-26 同日）与设计

1. **添加 / 编辑回忆的界面太简陋** → 编辑器升级为「星屿手稿」：左侧实时海报预览（封面、标题、日期、地点、放映风格徽章、季节调色与飘落预览），右侧四章：Ⅰ 故事、Ⅱ 影像（照片卡片网格，卡片上直接写描述）、Ⅲ 放映（三张带循环示意动画的风格卡片 + 季节选项）、Ⅳ 乐章；章节标题使用罗马数字徽记 + 思源宋体 + Cinzel 副标，与放映厅、魔法书同一套金色语言。
2. **放映时可选春夏秋冬四个主题** → 每个季节 = 调色（柔光叠色 + 舞台滤镜）+ 光影（顶光 / 阳光光束 / 地面暖光 / 霜边）+ 粒子：

| 季节 | 调色 | 光影 | 粒子 |
|---|---|---|---|
| 春 | 粉桃柔光、饱和度 +6% | 顶部柔和晨光 | 樱花瓣：贝塞尔花瓣形，自转 + 绕纵轴翻面（scaleX = cos），随风横向飘 |
| 夏 | 暖金柔光、饱和度 +14%、对比 +3% | 右上角缓慢旋转的阳光光束（滤色） | 萤火 / 金色微光：向上漂浮、明灭闪烁 |
| 秋 | 琥珀柔光、轻微棕褐 | 底部暖光 | 枫叶：五裂叶形，翻滚（翻面 + 旋转）幅度更大，下落更快，四种红橙色 |
| 冬 | 银蓝柔光、饱和度 −28% | 四周霜边 | 雪：远 / 中 / 近三层，近处大而虚（散景），远处小而慢 |

- 依据：Boris FX BCC Snow（深度分层、大小与速度**各自有随机变化**避免机械感、轻微湍流）；AEJuice 花瓣（自转 + 随机初始角度 + 低重力高阻力的「轻飘」）；Toolfarm Creation Effects: Falling Leaves（叶子要「摇摆、翻折、三维旋转」）。
- 季节在编辑器里保存为回忆的默认值（可选「按月份」自动：3–5 月春、6–8 月夏、9–11 月秋、12–2 月冬），观看时可以在放映控制条里随时切换，粒子与调色 1.2–1.4 秒交叉渐变。
- 粒子数量随画面面积缩放；「柔和」档减半；「减少动态效果」只保留调色、不画粒子。

### 7.6 v1.7.1：城市回忆目录页（Owner 2026-10-27 反馈：点进城市后的回忆列表界面没有优化）

- 现状问题（实测截图）：左右交错的时间线两侧大量留白、卡片稀疏；卡片只有封面 + 标题 + 日期，看不到 v1.7.0 新增的放映风格 / 季节 / 预计时长；「新的回忆」卡片与空状态（米色羊皮纸）和编辑器「星屿手稿」风格不一致。
- 资料：Huemor《Timelines》——纵向时间线适合长内容与移动端，只放关键节点，节点要用醒目的标记便于扫读，用交互逐步展开细节；Kombai「Reel Fest」电影节节目单——标题为第一层级、时长为第二层级、类别用颜色标签表达，入场用 0.06s 错开的批量淡入。
- 结论：改为**单列时间线 + 章节卡片**（左海报、右信息），节点使用与编辑器相同的罗马数字章节徽记；卡片层级 = 标题 > 时间 / 时长 > 风格与季节徽章 > 摘录与缩影；「放映」作为主操作直接放在卡片上；空状态与「新的一页」改用深色烫金手稿语言。

## 8. 参考来源

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
- AppleInsider — Inside iOS 10: Photos Memories will generate slideshow movies automatically: https://forums.appleinsider.com/discussion/193614
- Photofocus — iOS 15 preview: create movie-like scenes with Memories: https://photofocus.com/mobile/ios-15-preview-create-movie-like-scenes-with-memories/
- Krumzi — How to make a photo slideshow with music: https://www.krumzi.com/blog/how-to-make-a-photo-slideshow-with-music
- Pic-Time — 6 tips to make beautiful photo slideshows: https://blog.pic-time.com/blog/6-tips-to-make-beautiful-photo-slideshows
- IT 之家 — 照片的「电影感」: https://www.ithome.com/0/680/706.htm
- BFI — Saul Bass: 10 essential title sequences: https://www.bfi.org.uk/lists/celebrating-saul-basss-centenary-10-essential-title-sequences
- MovieMaker — How Wong Kar-wai uses frames within frames: https://www.moviemaker.com/visual-framework-how-wong-kar-wai-uses-frames-within-frames
- Harry Potter Fan Zone — Meet MinaLima: https://harrypotterfanzone.com/exclusive-meet-minalima-part-1/
- Motion Array — How to animate flat 2D images (2.5D parallax): https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/
- Resistenza — Motion-ready fonts for animated titles: https://resistenzatype.fontdue.com/article/motion-ready-best-fonts-animated-titles
- Wikipedia — Kinetic typography: https://en.wikipedia.org/wiki/Kinetic_typography
- W3C — Requirements for Chinese Text Layout (clreq): https://www.w3.org/TR/clreq/
- Aquasoft — Fun with Polaroids: https://www.aquasoft.net/blog/en/?p=895
- Boris FX — BCC Snow: https://borisfx.com/documentation/continuum/bcc-snow
- AEJuice — How to make falling petals in After Effects: https://aejuice.com/blog/how-to-make-falling-petals-in-after-effects
- Toolfarm — Creation Effects: Falling Leaves: https://www.toolfarm.com/news/new-creation-effects-falling-leaves-is-now-available-at-toolfarm/
- Huemor — Timelines (glossary): https://huemor.rocks/glossary/timelines/
- Kombai — Reel Fest film festival design: https://kombai.com/gallery/inspirations/reel-fest/
