# Changelog

## [1.10.1] - 2026-10-29

### Changed — 时光长卷「时光之环」优化（Owner：太拥挤、卡片加载不出、太密时一直闪烁、延伸线违和）
- **远近分级**：只有焦点附近的几段是完整卡片（电脑焦点左侧 2 张、右侧 1 张；手机左右各 1 张），其余回忆收成环上悬着的**光珠**；焦点附近用「鱼眼」间距，卡片之间不再重叠，回忆再多也不拥挤。转动时光珠在焦点处展开成卡片、离开焦点时沿细线收回。
- **图片**：不再依赖浏览器懒加载（3D 变换下经常不触发），改为主动预取焦点附近的封面、解码完成后淡入；弱网时自动重试。
- **消除闪烁**：根因是每次签名地址到位都会触发整环重建，以及几十张卡片自转、正反面切换、层级来回抢占。现在数据真的变化才重建；卡片单面、只缓慢偏转与摆动；层级带滞回；静态环线缓存到离屏画布。
- **延伸线重做**：从终点顺着环的方向继续向前、微微外旋（从起点外侧掠过），渐细渐虚，淡入星空；线头一点光像仍在书写的笔；「TO BE CONTINUED · 未完待续」沿线排字（手机为「未完待续」），只在转到终点附近时出现。
- 从放映返回时回到离开前的那一段。手机竖屏的环更「立」，占满标题下方的空间。

### Added — 点击直达
- 点击任意**光珠 / 卡片 / 周年节点 / 底部刻度**，时光之环沿最短路径一次转过去（越远越久，最长约 1.25 秒）；距离远时途中卡片先收成光珠、到达后再展开。鼠标悬停光珠显示日期与标题。

### Added — 日期精确到日 · 我们的纪念日
- 编辑回忆的「时间」新增**日**（默认「不记得哪天」）；保存为 `YYYY-MM-DD`。只有年月的旧回忆照常显示与排序（按当月 1 日），编辑时会提示可以补上具体日期。时光长卷、城市相册、放映、时光剪影都按日显示与排序；同一天按创建先后。
- 时光长卷标题下新增「**纪念日**」徽记：编辑者可设置我们的纪念日（或恢复默认：以最早一段回忆为起点）。**周年节点按纪念日每年同一天**生成（2 月 29 日在平年按 2 月 28 日）；第一年包含纪念日之前的回忆；纪念日当天的回忆属于新的一年。

### Fixed — 时光剪影残留加载文字
- 准备照片超时（8 秒）开始放映后，迟到的照片会把「正在准备这一年的胶片 x / y」写回画面；现在开始放映即停止更新并淡出。时光剪影的日期范围与表盘位置精确到日。

### Changed — 魔法书页背景
- 魔法书页的背景与其他页面统一为**星空 + 深蓝**（之前是暖金色）；金色只保留在书本自身的光。

### Data
- 无 schema 变化、无 SQL。新增的可选字段都在现有 `book_data.payload` 内：回忆 `date` 允许 `YYYY-MM-DD`；`settings.anniversary`。旧数据无需迁移。

## [1.10.0] - 2026-10-29

### Changed — 时光长卷「时光之环」（Owner：直线时光轴改为三维环）
- 时光轴变成一枚**向页面纵深展开的三维环**：不闭合，起点与终点紧挨着、都在页面右侧；终点处一条线继续向外、向上飞出画面（「TO BE CONTINUED · 未完待续」），线上有向外流动的光点。拖动 / 滚轮 / ← → 转动整环（惯性、回弹、吸附到最近的站点），底部年轮刻度条保留。
- 每段回忆是**悬挂在环上的 3D 卡片**：细金线 + 正反两面（正面封面，背面金箔纹样与标题 / 日期 / 城市 / 照片数），缓慢自转、像钟摆一样轻轻摆动；转到焦点或鼠标悬停时转回正面。越靠后越小越暗，背景浮现焦点年份。

### Added — 周年节点与「时光剪影」
- 以第一段回忆的月份为起点，每满一年在环上加一个**周年节点**（发光星环 + 悬挂铭牌）；最后一个周年之后若还有回忆，末尾加「第 N 年 · 至今」节点。
- 节点上的 **ANNIVERSARY · 时光剪影** 按钮放映这一年的全部回忆，采用全新的风格：12 个月的**年轮表盘**为主线，照片先以**高反差剪影**出现再显影成彩色，篇章在胶片带 / 折扇 / 主镜三种版式间轮换，中途「这一年」数字与足迹，尾声表盘留一个缺口并延伸出一条线——未完待续。

### Changed — 背景音乐自动循环播放
- 数据就绪后立即尝试自动播放；浏览器不允许时，第一次点击 / 轻触 / **按键**（例如回车登录）即开始；循环播放；被系统打断、播放出错（地址过期）或从后台回来时自动恢复。

### Fixed — 发布脚本中文乱码
- `release-current.ps1` / `publish.ps1` 读取文件时显式使用 UTF-8（Windows PowerShell 5.1 默认按 GBK 读取无 BOM 的 UTF-8，导致 AGENTS.md、PROJECT_STATE.md、README.md、00-config 注释被写成乱码）；本版已恢复这四个文件。`check_project.py` 新增乱码检查。

### Data
- 无变化（只读现有回忆字段）。

## [1.9.2] - 2026-10-28

### Added — 放映「镜头语言库」（Owner：文字和照片的呈现形式太单一）
- **文字样式库**：标题卡（金色大字 + 幕序 SCENA · III + 饰线，放大收拢进场、散成星尘退场）、诗行（侧栏逐行擦出、竖金线）、引语（「 」引号展开、逐字升起）、低语（小字宽字距、焦外到清晰）、逐字点燃字幕、便笺纸条、日期邮戳；文字可随时间与照片反向漂移（视差）。
- **照片呈现库**：拱窗、画廊卡纸、侧栏羽化等画框；穿越 / 升起 / 显影 / 下沉等进退场；与文字互动——对焦（标题散去时照片由虚到实）、让位（照片缩到一侧为诗行让出空间）、压暗（引语出现时照片压暗）。
- **银幕**按照片横竖与描述长短从 8 种镜头中选择（满幅字幕 / 竖排 / 对焦标题 / 让位诗行 / 拱窗 / 画廊 / 引语 / 穿越），同一镜头不连续；组在横屏用「故事板」（组描述固定在左栏、照片在右侧依次溶接）。
- **星图**新增「主星」大相框页、短句标题卡与引语、进场 / 退场轮换；**手札**新增推入 / 抛落进场、和纸胶带 / 回形针装饰、便笺纸条与日期邮戳。

### Changed — 自动放映 = 电影模式（Owner：从头到尾流畅放完，不要进度条，按钮退下，鼠标到下方才出现）
- 放映前先下载并解码前 12 张照片（「正在准备胶片 k / n」，最多 8 秒），其余顺序后台解码，放映中不再因等照片停顿。
- 华丽档跟随屏幕刷新率渲染（修正 60Hz 屏幕上的半帧率抖动）；文字进场完成后不再每帧写样式。
- 自动放映不显示进度条与计数；放映中所有按钮（含左上菜单与返回）退下，鼠标进入画面下方 20% 时控制条从下方滑出；开场不闪现按钮。

### Added — 编辑器拖放编组（电脑）
- 把未编组的照片拖进组框 = 加入该组；拖动组内照片时组框下方出现「拖到这里 · 移出这一组」；拖到组外照片旁 / 空白处 = 移出；组框头把手可整组拖动；每次拖放可撤销。

### Data
- 无变化（不新增字段）。

## [1.9.1] - 2026-10-28

### Added — 照片分组「同一时刻」（Owner：同一时间地点里几张内容相近的照片，希望用一段文字描述，放映时浮现）
- 编辑器：选择模式下批量操作栏新增 **编为一组 / 加入这一组 / 合并为一组** 与 **移出分组**；一组照片显示为横跨整行的金色括线框，框头「第 N 组 · k 张」+ 整组前移 / 后移 / 拆组，框内有一段**组描述**（最多 300 字）。组内单张描述收起但保留，拆组后恢复。
- 排序规则：组内照片前移 / 后移在组内移动，到组边缘再向外 = 离开这一组；组外照片遇到组时整组跳过；电脑拖动到组内照片旁 = 加入该组。所有分组操作可撤销。
- 放映：组描述在这组第一张出现后浮现，一直停留到这组最后一张让位；长描述分句依次出现并铺满整组时长。**银幕**组内画面柔和溶接；**星图**每组独占一页、编号显示范围「03 — 05」；**手札**组内照片叠成一小叠、镜头停在中心、描述手写在下方。
- 预览统计与放映厅显示「k 组」；时长估算计入分组。

### Added — 自动放映 / 手动放映（Owner：放映应该有自动和手动两种）
- 放映厅新增「MODE」一行：**自动放映**（原有行为）/ **手动放映**；放映控制条新增模式按钮，放映中可随时切换；选择记在本机（`sb-play-mode`）。
- 手动放映：每张照片播完入场与描述后，**在描述完整显示时停住**，右侧出现呼吸的「› 继续」提示；点击画面 / → / Enter / 轻触右侧 / 左滑 = 下一张（3 倍速平滑播到下一张转场），← / 轻触左侧 / 右滑 = 上一张；描述没读完时翻页直接切到下一张；最后一张后进入「终」页。分组照片逐张停靠，组描述保持显示。

### Changed — 世界星图搜索
- 搜索结果下方不再显示「数据：国家统计局 / 高德 … 」来源行（署名移到 README「数据来源」）。

### Data
- 放映方式是本机观看偏好（localStorage `sb-play-mode`），不写入回忆数据。
- 回忆新增可选字段 `groups: [{id, text}]`，照片新增可选字段 `g`（组 id）；存放在现有 `book_data.payload` 中，**无需 SQL / migration**，旧回忆不受影响。

## [1.9.0] - 2026-10-28

### Added — 地球搜索补齐行政区划（Owner：很多城市搜不到）
- 新数据块 `blocks/06-admin-divisions.html`（`tools/make_admin.py` 生成）：**中国** 34 个省级、334 个地级、2845 个县级（县级市 / 区 / 县 / 旗）；**美国** 51 个州（含华盛顿特区）、3144 个县。来源：Vonng/adcode（国家统计局 2016 区划 + 高德地理中心）、美国人口普查局 2010 县几何中心（btskinner/spatial）、kjhealy/fips-codes。
- 支持全名、简称（湖南 / 长沙 / Orange）、州缩写（TX）与常见中文简称（加州、德州、麻省…）；结果新分组「州省 · 市县」并标注层级与上级；选中后地球飞转到对应位置并高亮国家。

### Added — 回忆编辑器「影像管理台」
- 工具栏：照片数、**批量添加**、**选择**、卡片 / **紧凑**视图切换（记住偏好）。
- 批量添加：多选或整章拖入，排队并发 2 张上传，整体进度条，失败可重试 / 忽略。
- 选择模式：勾选框、Shift 区间选择、全选 / 反选 / 取消；底部**批量操作栏**：设为封面、移到最前、移到最后、清空描述、删除（二次确认）；删除与清空描述 6 秒内可**撤销**。
- 电脑上可直接拖动照片排序（金色插入线）。
- 可扩展：批量操作是注册表 `SB.editor.photoActions`，以后加「旋转」「移到其他回忆」只需追加一项。

### Changed — 登录加载界面「星盘启封」
- 重新设计：夜空 + 多层旋转星盘（刻度环、星点环、虚线环、八芒星、扫光加载环、呼吸宝石），状态行「正在连接星海… / 正在翻开书页…」交叉淡入；登录态星盘缩小上移，下方淡入带四角花饰的登录卡片。
- **字体不再中途变化**：文字在字体决策完成后统一淡入；2.2 秒内网络字体到齐就用网络字体，否则整个启动过程固定使用本地宋体。
- **不再卡顿**：动画只用 transform / opacity（合成器线程），去掉旋转元素上的滤镜与卡片背景模糊；登录门遮住画面时不运行背景粒子。

### Governance
- 新 Prompt `prompts/00-login-gate.md`；更新 `prompts/07-globe.md`、`prompts/12-memory-editor.md`、`prompts/00-architecture.md`；`docs/design/VISUAL_UPGRADE_PLAN.md` 第 13 节。
- `tools/check_project.py`：新增行政区划数据、批量操作注册表、启动门字体决策检查。

### Data
- **无数据库、RLS、schema_version、Book 数据结构或 Storage 变化；无需 SQL。** 批量操作只修改编辑中的 `slides` / `cover`，保存与文件清理逻辑不变。


## [1.8.3] - 2026-10-27

### Changed — 开书第一阶段丰富为「机关启封」（Owner：宝石亮起 + 一圈光环太淡）
- **机关逐级啮合**：外圈刻度环 → 齿轮环（反转）→ 三枚小齿轮（自转 + 公转）→ 内星环每隔 0.16s 依次启动，**棘轮式**每秒 4 次「咔哒」步进，1.2s 内加速到 6–8 倍。
- **宝石旋转**：宝石作为动力核心从静止加速到约 1 圈 / 秒，并做两次轻微呼吸缩放。
- **能量沿烫金流动**：法阵外圆、内圆、八芒星被香槟金细线依次描亮，两颗光珠沿内外圆反向奔跑。
- **星辰依次点亮**：八颗蓝宝石星绕圈依次放大闪亮。
- **机关火花**：宝石外圈沿切线迸出细小金色火花（正常混合，很快熄灭）。
- **符文环加速**并在启封时向外扩散淡出；1.2s **双重共鸣**光环；1.5s **解锁**：四角包角弹开闪亮、书身轻震、书页切口透出一线暖光。
- 之后衔接 v1.8.2 的启封（扉页金墨星图 + 星尘）与门钥匙；总长约 4.7 秒。仍然不汇聚、不闪白；手机同样可完整播放（火花减量、描线两条）。

### Governance
- `prompts/04-book-opening.md` 追加 v1.8.3 时间表；`docs/design/VISUAL_UPGRADE_PLAN.md` 第 12 节。

### Data
- **无数据库、RLS、schema_version、Book 数据结构或 Storage 变化；无需 SQL。**


## [1.8.2] - 2026-10-27

Owner iPhone 真机反馈修订（定位与设计：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 11 节）。

### Added
- **回到魔法书**：右上角标识组最左侧新增「书本」标识，点击直接回到魔法书封面（熄灯器转场）；在魔法书页面自动隐藏。不放进左上菜单。

### Changed — 开书特效重做「星尘启封」
- 不再有任何粒子汇聚、穿越光线或闪白：唤醒（宝石柔和充能 + 一圈细光环）→ 启封（封面打开、纸页翻动，**扉页上金墨自己画出一幅星图**，星尘从书页四周向上飘散）→ 入页（推进书页 + 门钥匙暮色漩涡）。约 3.7 秒。

### Fixed — 手机性能与渲染
- **开书冻结后直接跳转**：开书期间不再预取地球（会同步创建 WebGL 并编译着色器，仿真长任务 6–17 秒）；地球改在门钥匙盖满画面后准备。
- **书上方刺眼光球**：薄烟粒子从叠加混合改为正常混合、低透明度，只在华丽档出现。
- **封面对角切割与闪烁**：3D 符文环改为 2D 投影（书前 / 书后两层），不再与书本 3D 平面相交。
- **魔法书动态卡顿**：柔和档（手机默认）关闭星云、体积光、折射、流光遮罩、烫金辉光层、书口流光等昂贵层，烫金使用廉价滤镜，小齿轮不再触发 SVG 滤镜重绘，背景法阵静止；导航 / 标识 / 菜单在柔和档不用背景模糊。
- **首页加载慢**：皮革 / 纸张程序纹理缓存到本地（第二次打开即时）；放映器纹理推迟到第一次进入放映时生成。
- 手机上右上角标识缩为 32px，与左上按钮、返回光球同排不重叠。

### Governance
- 更新 Prompt：`prompts/04-book-opening.md`（重写）、`prompts/03-magic-book.md`、`prompts/02-menu.md`、`prompts/performance/02-book-to-globe.md`。
- `tools/check_project.py`：禁止开书期间预取地球；符文环必须是 2D 前 / 后图层。

### Data
- **无数据库、RLS、schema_version、Book 数据结构或 Storage 变化；无需 SQL。** 浏览器本地新增两项纹理缓存（`sb-tex-leather-v182`、`sb-tex-paper-v182`），可随时清除。


## [1.8.1] - 2026-10-27

Owner 实看 v1.8.0 后的反馈修订（调研与设计：`docs/design/VISUAL_UPGRADE_PLAN.md` 第 10 节）。

### Visual — 去除过曝
- **开书汇聚不再刺眼**：逐帧实测发现全局粒子、环绕光带、魔法书烟雾 / 火星都用叠加混合并被吸向宝石同一点，亮度失控。现在粒子越接近汇聚点越透明（被宝石「吸收」），汇聚时整体亮度设上限；冲击光环、宝石光晕、书页光柱、穿越光线全部减弱；开书后的书页亮度降低。
- **进入世界星图不再闪白**：门钥匙的全屏光幕从近白色改为暮色（深靛蓝 + 中心琥珀光门，峰值亮度约 60%）。
- 写入曝光硬规则：全屏遮罩只能用深色，亮色只能是局部光源，叠加层 alpha ≤ 0.55，汇聚粒子必须随距离淡出。

### Visual — 分路转场、放慢光线
- 每条路线一种门：魔法书 / 菜单 → 地球 = **门钥匙 · 暮色漩涡**；地球 → 国家 = **幻影显形**；国家 → 城市、→ 时光长卷 = **墨金书页**（新：一页深色书页带香槟金书边从右向左翻过）；城市 / 时光长卷 → 放映 = **冥想盆**（新：银蓝涟漪 + 缓慢倾斜的记忆丝缕，放映厅从「水面」浮现）；返回 = **熄灯器**。
- 所有光丝 / 彗星 / 涟漪速度约为 v1.8.0 的 55%，改用 easeInOutSine 柔和曲线；单次转场 1.4–2.0 秒。

### Visual — 魔法书「星夜摩洛哥皮」
- 皮革改为午夜靛蓝摩洛哥山羊皮（细密荔枝纹 + 低频旧化斑驳 + 冷色划痕）；烫金改为低饱和的**香槟古金**；新增不上金的**盲压 dentelle 花边**与法阵外圈盲压圆点；法阵八个顶点镶嵌会轻轻闪烁的**星辰蓝宝石**；古金雕花包角 + 蓝宝石铆钉；金口书页、机匣齿轮、内封衬页同步换色。
- 渲染：左上主光、右下冷色轮廓光、法阵凹陷环境光遮蔽、冷白皮革反光；书下光晕改为淡金并减弱。

### Layout — 菜单与右上角三枚标识
- 左上菜单只保留 **世界星图** 与 **时光长卷**（原「回忆总览」）；删除「合上魔法书」「七大洲」。
- 新块 `blocks/02y-dock.html`（`SB.dock`）：每个页面右上角三枚 36px 无文字标识——**音乐**（开关、曲名、播放时跳动音柱；可编辑者在此试听 / 上传 / 更换 / 移除全站音乐）、**动效**（华丽 / 柔和 / 静止 三档）、**账户**（邮箱、身份、当前书、退出登录）。一次只开一个面板；放映进行中跟随放映控件隐藏 / 显示并下移避让。

### Layout — 「时光长卷」时间轴
- 「回忆总览」改为全屏横向**时光长卷**：流动的金色时光河、上下交替的相片卡（4:5 相框 + 字幕）、星形节点与月份刻度、背景大号年份描边数字视差、景深（离中心越远越小越暗并转向中心）、底部**年轮刻度条**（可点击 / 拖动跳转并显示当前可见范围）。
- 鼠标拖动（惯性 + 两端回弹）、滚轮、触控滑动、键盘 ← → / Home / End；入场时时光河描出、卡片依次升起；默认停在最新的回忆。点击卡片用冥想盆进入放映，返回时回到时光长卷；点击城市胶囊用墨金书页进入城市。场景 id 仍为 `overview`（深链兼容）。

### Layout — 城市空状态
- 空城市不再是悬在法阵中央的方形大卡片：改为与章节卡片同比例的「空白章节卡」——电脑左侧 3:4 空相框（流动虚线框 + 星屿压印 + ＋）、右侧 CHAPTER I · 第一章 / 标题 / 引导语 / 「写下第一章」；手机相框为 4:3 横幅置顶。页眉统计显示「0 段回忆 · 等待第一章」。

### Governance
- 新增 / 更新 Prompt：`prompts/00-gate.md`（重写）、`prompts/02-menu.md`（重写，含 `SB.dock`）、`prompts/13-overview.md`（重写为时光长卷）、`prompts/04-book-opening.md`（柔光版）、`prompts/03-magic-book.md`、`prompts/01-ambient-fx.md`、`prompts/10-city-album.md`、`prompts/00-architecture.md` 追加 v1.8.1 内容。
- `tools/check_project.py`：门接入检查改为分路 `gate.cover(gateKind`；新增 `SB.dock`、时光长卷、菜单精简的回归检查。

### Data
- **无数据库、RLS、schema_version、Book 数据结构或 Storage 变化；无需 SQL。** 放映参数新增可选的 `from:'overview'`（仅 URL / 历史状态，用于返回到时光长卷）。


## [1.8.0] - 2026-10-27

### Visual — 「秘境之门」奇幻转场（VIS-002）
- 新块 `blocks/01b-gate.html`（`SB.gate`，全屏画布 `#sb-magic-gate`），只替换 Scene Runtime 的 cover / reveal 视觉，事务顺序不变（`prepare → cover → await enter → nextPaint → reveal → cleanup`）。
- **门钥匙 Portkey**（`flash`：魔法书 → 地球、菜单 → 地球）：40–60 条金色光丝沿螺线旋入，暖白蒸汽团旋转，中心光门扩大盖满全屏；等待目标场景时光幕上有缓慢旋转的符文环；揭示时光门从中心「撕开」（羽化 + 不规则边缘），光丝反向甩出。开书时光门从书页中心打开。
- **幻影显形 Apparition**（`portal`：点击处圆形揭示）：准备阶段点击处出现旋转的小符文环（取代纯光圈）；揭示时圆形边缘带双圈刻度符文环、6 条螺旋金丝、外侧柔光与向外飞溅的火星。
- **熄灯器 Nox / 荧光闪烁 Lumos**（`veil`：返回、菜单跳转）：光点像彗星一样被吸向中心、夜色收拢、最后一点光熄灭；揭示时中心荧光闪烁亮起，光推开夜色，彗星向外散开。
- `SB.gate` 不存在时自动回退到旧的 veil / flash / 光圈；任何准备失败都会 `SB.gate.abort()` 清理，不留遮罩；bfcache 恢复同样清理。reduced 档不显示门。

### Visual — 「星辉层次」魔法书与地球（VIS-003）
- **魔法书**：星云、宝石光溢与旋转光束、绕书一圈的 3D 符文环（28 / 16 枚，经过封面中央时自动变暗）、烟雾与火星（画布粒子，low 档减量、reduced 关闭）、书页边缘流光、新增能量脉络；开书时烟雾、火星与符文环被吸入宝石。
- **地球**：海面星辉高光、程序生成的云雾层、外层呼吸光晕、星座线、倾斜星盘环（拉丁铭文刻度）、按时间连接我们城市的「足迹光弧」与流动光点。

### Navigation / Search（NAV-001）
- **删除大洲国家目录页**（`blocks/08-continent.html`、`prompts/08-continent.md`）：国家地图的父级改为世界星图，左上角返回 / 面包屑 / 系统返回都直接回到地球，地球自动转向刚才的国家并短暂高亮。
- 地球上的大洲徽章、手机底部大洲按钮和菜单「七大洲」改为**让地球转向该大洲**。
- **地球正上方新增搜索栏**：可搜索我们的城市、任意国家与任意城市；内置 648 座城市离线库（`blocks/06-world-cities.html`，由 `tools/make_cities.py` 从 CLDR 中文城市名 + IANA zone.tab + 手工补充生成）+ 在线城市搜索（Open-Meteo Geocoding，中文，350ms 防抖、6 秒超时、可取消、缓存；失败时只显示本地结果）。
- 选中结果后地球以 easeInOutCubic 沿最短方向快速转到目标并推近，目标国家高亮、目标点亮起星标与扩散光环，下方浮出信息卡（「打开我们的回忆」/「进入 X 地图」）。支持键盘 ↑↓ / Enter / Esc。

### Governance
- 新增 / 更新 Prompt：`prompts/00-gate.md`（新）、`prompts/00-architecture.md`、`prompts/03-magic-book.md`、`prompts/07-globe.md`、`prompts/09-country-map.md`、`prompts/performance/03-globe-to-country.md`；调研见 `docs/design/VISUAL_UPGRADE_PLAN.md` 第 8 节。
- `tools/check_project.py`：DOM id 重复改为错误；新增 `SB.gate`、Scene Runtime 门接入、离线城市库、禁止大洲目录页回归的检查。

### Data
- **无数据库、RLS、schema_version、Book 数据结构或 Storage 变化；无需 SQL。**
- 新增唯一外部服务：Open-Meteo 城市搜索（只发送用户输入的搜索词，不发送任何回忆数据；不可用时功能降级为离线城市库）。


## [1.7.3] - 2026-10-27

### Performance / Stability
- **Scene Transaction 重构**：目标场景统一按 `prepare → cover → await enter → nextPaint → reveal` 生命周期切换，修复 async enter 未完成就揭罩造成的空背景、错页闪现和旧页残留。
- **登录 → 魔法书**：Gate 直到 Store JSONB、Book scene 与首帧 paint 完成后才退场；Store 启动不再全量创建整本书所有媒体 Signed URL。
- **魔法书 → 地球**：Three.js 脚本 idle 预热，Globe 增加 `prepare()`；手机降低 WebGL 初始化几何细分、纹理尺寸和粒子数量，Flash 只在地球首帧准备完成后退场。
- **地球 → 国家**：Globe hover 与 Continent focus/pointerenter 提前预取国家地图；Country `prepare()` 复用地图缓存，`enter()` 由 Scene Runtime await。
- **国家 → 城市 → 回忆**：City 首屏 cover 批量签名；Player `prime()` 可 await 并在 portal 揭示前预热封面/前几张照片；Editor 后台批量预取已有照片 URL。
- **Portal 稳定层**：Portal 使用 stage 内 backdrop 隔离旧场景，目标 scene 完成首帧后再圆形揭示；转场结束强制清理 clip-path/ring/backdrop。

### Governance
- 新增 `prompts/performance/` 下 5 份逐链路性能 Prompt，分别约束 Login→Book、Book→Globe、Globe→Country、深层页面和 Scene Runtime。
- `docs/PERFORMANCE_GUIDE.md` 升级为 v1.7.3 场景事务基线。

### Data
- **无数据库、RLS、schema_version 或 Storage 路径变化；无需 SQL。**


## [1.7.2] - 2026-10-27

### Performance
- **场景切换去残影**：`portal` 转场不再让旧场景保持 `is-active` 到动画结束；旧场景在新场景进入后立即卸载，圆形展开继续保留原有视觉语言，但不再出现上一页在新画面后方短暂滞留。
- **转场调度优化**：veil / flash / portal 改为按性能档位使用更短的动画时长，并在 scene swap 后等待浏览器完成下一次 paint 再继续退场，降低切换时主线程拥塞与“卡一帧”。
- **移动端自动性能档**：综合 coarse pointer、viewport、CPU core、device memory 判定 low / high；低性能设备降低全局粒子数量、Canvas DPR 和动画帧率。
- **放映时资源让路**：进入回忆放映后，全局 Ambient FX 自动降帧；播放器自身在 low / mobile 档限制到约 30 FPS，桌面高性能档保持 60 FPS。
- **照片加载预热**：进入放映厅前批量补齐 Signed URL，并预解码前几张照片；播放中预取窗口由 7 秒扩展到 12–16 秒，降低手机弱网下“正在冲洗胶片”的等待频率。
- **城市相册图片减载**：手机 / low 档减少每个章节卡片同时生成的缩影数量；仅首张封面 eager + high priority，其余封面 / 缩影 lazy + low priority；离屏章节启用 `content-visibility:auto`。
- **编辑器图片懒加载**：照片网格改为 `loading="lazy" + decoding="async" + fetchpriority="low"`，避免打开编辑器时一次性解码全部照片。
- **Private Storage 浏览器缓存**：新上传的唯一文件路径改为一年 `cacheControl`，减少重复打开同一照片时的网络开销。

### Responsive
- 城市章节卡片在手机端海报比例由 16:9 调整为 3:2，窄屏进一步使用 4:3，减少竖图被过度裁切。
- 回忆编辑器桌面端增大可用宽度并让预览列自适应；手机端增大预览尺寸，≤430px 时照片编辑卡片改为单列 3:2，提升可编辑面积。
- 放映厅手机端海报尺寸与垂直间距重新约束；竖屏 Cinema 黑边减少，让照片获得更多有效画面高度。
- low 档移除编辑器 / 通用弹窗实时 backdrop blur，并减少编辑器季节粒子数量，保持视觉风格但降低 GPU 压力。

### Governance
- v1.7.2 明确为性能与响应式优化版本；原计划的「秘境之门」视觉转场设计延期，避免在周年 Feature Freeze 前继续叠加特效。
- 新增 `docs/PERFORMANCE_GUIDE.md`，记录场景、图片、Canvas、响应式和未来 Agent 的性能约束。
- `tools/check_project.py` 增加关键性能回归标记检查。

### Data
- **无数据库、RLS、schema_version、Book 数据结构变化；无需 SQL。**
- 不迁移、不删除现有城市 / 回忆 / 照片 / BGM；Storage 仅影响 v1.7.2 之后新上传对象的浏览器缓存元数据。

## [1.7.1] - 2026-10-27

### Changed
- **城市回忆目录页升级为「星屿手稿 · 目录页」**（VIS-008，只改块 10），与回忆编辑器同一套视觉语言：
  - 页眉：缓慢旋转的金色法阵、城市名、四芒星金线、统计胶囊（回忆数 / 照片数 / 时间跨度）、「新的回忆」按钮；
  - 左右交错时间线改为**单列金色时间线**，节点为罗马数字章节徽记 + 竖排年月；
  - **章节卡片**：烫金海报（风格 / 季节徽章 + 季节调色，悬停光泽）、CHAPTER 编号与日期、标题、照片数 / 预计放映时长 / 风格与季节 / 配乐、一段话摘录、最多 5 张照片缩影；卡片上直接「放映」（直接开始）、「放映厅」、「编辑」；
  - 时间线末尾「写下第 N 章」新页卡片；空状态改为深色烫金「空白章节」（不再是米色羊皮纸）；
  - 手机：时间线贴左、海报变横幅、放映按钮独占一行（触控 ≥ 44px）。
- 卡片入场动画增加保险：动画结束（或个别设备上未启动）后移除动画，保证卡片一定可见。
- `prompts/10-city-album.md` 重写；`docs/design/VISUAL_UPGRADE_PLAN.md` 新增 7.6 节；转场 / 魔法书与地球特效顺延为 v1.7.2 / v1.7.3。

### Data
- **无数据库、RLS、Storage 变化；无需运行 SQL；只读取已有字段。**

## [1.7.0] - 2026-10-26

### Added
- **「光影放映」多图编排放映引擎**（VIS-005）：每种风格是一位「导演」，把照片编排成声明式时间线；画面里常有 2–3 张照片**接力**更替（一张留着、一张渐隐、新的一张渐显），不再一页一张。单张焦点约 3.2–3.6 秒，只有描述较长时才多停留。
- **三种放映风格**：
  - 银幕（默认）：宽银幕全幅镜头 + 双联 / 三联分屏；光缝、虹膜、百叶、擦入、光晕溶解、错位竖条、面板扩展为全幅、像门一样向两侧打开等转场；分屏中正在讲述的照片提亮；短句竖排大字幕、长句下三分之一大字幕（字距收拢 + 逐字去模糊 + 金线）。
  - 星图：星空中 2–3 张烫金相框前后漂浮、视差与轻微 3D 倾斜，接力更替时旧照片化作星尘、新照片光晕显影，金线把相邻照片连成星座；字幕为编辑式大号编号 + 逐行遮罩升起。
  - 手札：烛光皮革书桌，相片逐张从空中落下（回弹 + 阴影 + 微尘）、堆叠，镜头沿桌面跟随最新相片；旁白像羽毛笔逐字写出（湿墨金光渐干），火漆星章点缀。
- **四季主题**（VIS-006）：春（樱花瓣翻飞、粉桃柔光）、夏（阳光光束、萤火）、秋（枫叶翻滚、琥珀暖调）、冬（三层雪花、银蓝霜边）；放映厅与放映控制条可临时切换，粒子与调色交叉渐变；按月份自动选择季节。
- 回忆**可选字段** `style`、`season`（缺省 `cinema` / `auto`）。
- 放映厅新增「STYLE / SEASON」选项（只影响本次观看）与随风格变化的预计时长。
- `SB.cinema`（风格 / 季节定义与图标）；`SB.player.setStyle / setSeason / stepSeason / estimate`。

### Changed
- **回忆编辑器升级为「星屿手稿」**（VIS-007）：左侧实时海报预览（封面、标题、日期、地点、风格 / 季节徽章、季节调色与飘落预览、照片数与预计时长）；右侧四章——Ⅰ 故事、Ⅱ 影像（照片卡片网格，直接在卡片上写描述，前移 / 后移 / 封面 / 移除）、Ⅲ 放映（三张带循环示意动画的风格卡片 + 季节选项）、Ⅳ 乐章。手机为单列。
- 扉页标题与一段话字号加大；扉页最长 9 秒。
- 跳转（上一张 / 下一张 / 进度条）改为跳到照片焦点时刻，并用 0.5 秒暗场衔接。
- `prompts/11-memory-player.md`、`prompts/12-memory-editor.md` 重写；`docs/design/VISUAL_UPGRADE_PLAN.md` 新增第 7 节调研与候选对比；转场与魔法书 / 地球特效顺延为 v1.7.1 / v1.7.2。

### CI / Governance
- `tools/check_project.py` 放映回归检查增加 `SB.cinema`。
- 新增版本发布脚本 `scripts/releases/release-v1.7.0.ps1`。

### Data
- **不需要运行 SQL，不改 schema_version，不迁移旧数据。** 新字段只在编辑并保存回忆时写入；旧回忆按默认风格 / 按月份季节放映。

## [1.6.0] - 2026-10-26

### Added
- **「冥想盆放映厅」电影式回忆放映**（VIS-004）：
  - 放映厅：封面海报（烫金细框）、日期 / 标题 / 地点、照片张数与预计时长、带旋转符文环的「放映」按钮。
  - 开场：熄灯与放映机启动闪烁、银幕黑边落下（横屏约 1.85:1，竖屏 7% 画框）、墨滴入水 + 三圈涟漪、扉页逐字浮现。
  - 镜头：按照片比例自动选择推镜 / 拉镜 / 横摇 / 纵摇 / 悬浮相片，正弦缓动，放大不超过 1.12。
  - 转场：光尘溶解（默认 1.6s）、暖金光漏（每 4 个镜头与最后一个镜头）、墨滴揭幕（第一张）；手动翻页 0.8s。
  - 电影字幕：按 Netflix 简体中文规范（每行 ≤16 字、≤2 行、金字塔断行），按每秒 7 字计时，逐字柔和浮现；照片停留时间自动延长到字幕读完。
  - 终章：暖金闪白 → 「终 · FINIS」、日期地点、「再放一遍 / 返回相册」；音乐 3 秒内渐弱到 30%。
  - 胶片颗粒、暗角、金色光尘；分段进度条可点击跳转；滑动 / 键盘 / 空格控制；切到后台自动暂停。
- 城市相册卡片右下角新增「放映」按钮，直接开始放映。
- `SB.audio.duck(level, ms)` 音量平滑压低 / 恢复。
- `SB.player`（play / seek / jump / state）供测试与调试。

### Changed
- `prompts/11-memory-player.md` 重写为 v1.6.0 放映提示词；`docs/design/VISUAL_UPGRADE_PLAN.md` 新增第 6 节电影式放映参数调研。
- 照片等待签名地址最多 5 秒，期间显示「正在冲洗胶片…」，并预加载解码后续照片。
- 低性能（动效「柔和」）去掉模糊与胶片颗粒；系统「减少动态效果」只保留淡入淡出。

### Data
- **无数据库、RLS、Storage 变化；无需运行 SQL；只读取已有回忆字段，不影响任何已有回忆数据。**

### CI / Governance
- 新增 `release-current.ps1`：以后完成版本迭代后只需从 `VERSION` 自动识别版本并一键进入发布链路。
- 自动生成缺失的 `docs/releases/vX.X.X.md` 基础记录，以及版本审计脚本 `scripts/releases/release-vX.X.X.ps1`；已有 Release Record 不覆盖。
- `publish.ps1` 在被直接调用时也会从模板补齐缺失 Release Record，修复“required governance/release files missing”发布中断。
- `check_project.py` 的 `OK` 改为所有治理校验真正通过后才输出，并增加旧 `data/db.json` / GitHub runtime persistence / `SB.book` 视觉对象回流硬保护。

## [1.5.2] - 2026-10-26

### Fixed
- **字体“乱码”根因修复**：移除 ZCOOL XiaoWei。该字体的「回 圃 圄 圊 崮 徊」字形自身损坏，在 Chromium / FreeType 下渲染为实心方块，导致「回忆总览」等显示为「■忆总览」；且只覆盖约 7000 字，罕见字会混入其他字形。
- 移除 Cinzel Decorative：数字「1」显示为罗马式「I」，小字号花体难以辨认。
- `✦ ✎ ✕ ⟲` 等在网页字体中不存在的符号全部改为内联 SVG 图标，手机上不再回退成 Emoji 或空心方框。
- 标题中的分隔点「·」不再出现在行首。

### Added
- 「星文」字体系统：中文统一思源宋体（Noto Serif SC 400/600，封面书名 900 按字子集加载）、拉丁铭文 Cinzel、数字与日期 Cormorant Garamond。
- 排版令牌：字号阶梯 `--fs-*`、行高 `--lh-*`、字距 `--tr-*`、字重 `--fw-*`；`.sb-num`、`.sb-rune`、`.sb-foil` 工具类。
- `SB.icon(name)` 内联 SVG 图标集（spark / star / quill / close / reset / plus / minus / up / down / chevron / note）。
- `SB.ui.button(text, kind, onClick, icon)` 可选图标参数（向后兼容）。
- `SB.fmtTitle()` 标题分隔点防断行；`SB.type.ready` 字体预热。
- `docs/design/VISUAL_UPGRADE_PLAN.md`：v1.5.2 → v1.6.2 视觉升级计划、乱码实测与调研来源。
- `prompts/00-typography.md`：字体系统提示词。

### Changed
- 所有场景标题、按钮、标签、菜单、提示条、弹窗改用 `--f-display`；居中大字距标题增加光学居中补偿。
- 总览统计、时间线日期、放映页码等数字改用 Cormorant Garamond 等高数字。
- 魔法书封面 SVG 文字改用思源宋体 900 / Cinzel，铭文分隔改为 `·` 与绘制的四芒星。
- Supabase 客户端 `x-client-info` 改为读取运行时配置版本号。

### CI / Governance
- `tools/check_project.py` 新增字体回归检查：构建产物中出现 ZCOOL XiaoWei、Cinzel Decorative 或 `✦ ✎ ✕ ⟲` 时校验失败；并检查 `SB.icon` 存在。

### Data
- **无数据库、RLS、Storage 变化；无需运行 SQL；不影响任何已有回忆数据。**

## [1.5.1] - 2026-10-26

### Added
- 根目录 `README.md`，为 GitHub 与人工阅读提供简短入口，并明确新 Agent 从 `AGENTS.md` 开始。
- `supabase/migrations/002_v151_title_and_members.sql`：非破坏性更新当前 Book 标题，并加入两名 `editor` 成员。
- 当前 Book 新增 editor：`11aa32fe-3875-4880-81fb-02a543dca853`。
- 当前 Book 新增 editor：`62adee54-c59a-4844-abb5-1b5629da3bf9`。
- 根目录 `AGENTS.md`，作为所有新 Agent / 新开发会话的强制上下文入口。
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`，固化需求 → 分支 → 校验 → PR → main → Pages → 数据保留 → 回滚的完整项目链路。
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`，固化多用户、多 Book、多 Relationship、多 Theme、多 Experience 的长期扩展边界。
- `docs/DATA_LIFECYCLE.md`，明确 Git/Pages 与 Supabase 数据生命周期分离以及向前 migration 原则。
- `docs/PROJECT_DOCS_INDEX.md` 与 `docs/templates/RELEASE_RECORD_TEMPLATE.md`。
- `docs/V151_OPERATOR_STEPS.md`，明确本次发布、Supabase migration 与 Production smoke test 的 Owner 操作。
- `docs/releases/v1.5.1.md` 完整 Release Record。
- 正式纳入 `validate.yml`、`deploy-pages.yml` 与 `publish.ps1` 的长期发布链路说明。

### Changed
- 当前 Anniversary Book 展示名称由《我们的星屿》统一为《星屿之书》，包括 Supabase `books.name`、登录权限提示、初始化 seed 与当前项目文档。
- `main` 正式定义为唯一 Production branch；release/feature 分支只通过 PR 进入 main。
- 每个版本必须记录 Product、Runtime、Architecture、Data、Auth/RLS、Storage、CI、Git/PR、Pages、Agent Governance 等链路变化；无变化也必须显式声明。
- 发布检查升级为“代码 + 文档治理”双重校验。

### Fixed
- 修复 Windows PowerShell 下 `publish.ps1` 的 Secret 扫描：`site/.nojekyll` 等空文件会让 `Get-Content -Raw` 返回 `$null`，此前会在 `.Contains()` 处中断发布。现仅扫描文本资源并显式跳过空内容。

### CI / Governance
- `tools/check_project.py` 开始检查 VERSION、Release Record、CHANGELOG、PROJECT_STATE 和核心治理文档一致性。
- `validate-starbook` 在 PR 上执行 build、项目检查和高风险 Secret 扫描。
- `publish.ps1` 发布前要求当前版本文档完整，避免无记录发布。

### Data
- **无 schema 结构变化，`schema_version` 保持 1。**
- 发布 v1.5.1 后需运行一次 `supabase/migrations/002_v151_title_and_members.sql`。
- Migration 仅更新 `books.name` 并 upsert 两名 editor；**不会修改 `book_data.payload`，不会删除/重建 Storage，不需要重新导入城市/回忆/照片/BGM。**
- Supabase 现有数据继续由同一 Book ID / Private Storage 承载。

## [1.5.0-anniversary] - 2026-10-26 (in progress)

### Added
- Supabase Anniversary Bridge 基础架构。
- `SB.user`、`SB.book`、`SB.theme`、`SB.experience` Runtime Context。
- Email + Password 私有登录门；周年版不开放公众注册。
- `books` / `book_members` / `book_data` Supabase schema 与初始化 SQL。
- Private Storage `starbook-media` 与基于 Book Membership 的 RLS。
- Private Storage Signed URL 内存缓存。
- `book_data.revision` 轻量并发冲突检测。
- 浏览器 `pushState` / `popstate` 场景历史支持。
- 版本文件、Roadmap、Project State 与 Release Record 制度。

### Changed
- `SB.store` 从 GitHub PAT / GitHub Contents & Git API 改为 Supabase Bridge Store。
- V1 `cities / memories / settings` JSON 数据结构保持不变，改存于 `book_data.payload`。
- 图片和音乐改为按 `{book_id}/images`、`{book_id}/audio` 保存到 Private Storage。
- 音乐周年版改为直接上传常见格式，不再浏览器转码。
- App 启动改为 Auth → Book Context → Store Ready → Scene Boot。

### Removed
- 周年正式运行路径中的 GitHub PAT 编辑钥匙。
- GitHub 仓库作为运行时数据库/媒体存储的依赖。
- `mp4-muxer` 音乐转码依赖。

### Security
- 浏览器端仅配置 Supabase Publishable Key。
- 未认证用户无法通过 RLS 读取 Book Data 或 Private Storage。
- Owner / Editor / Viewer 权限开始由 `book_members` 决定。

### Pending Verification
- Supabase migration / owner seed / Private Bucket 已在真实 Project 中执行并确认。
- 仍需真实 Auth 登录、前端 RLS、Storage 上传与手机端测试。

### Phase 3 Stability
- 移动端全局高度改为 `100dvh` 优先，并加强 safe-area / coarse pointer 触控目标。
- 动态脚本加载增加单源超时机制，Three.js 扩展为 cdnjs / jsDelivr / unpkg 三源回退，避免单个 CDN 长时间挂起。
- 浏览器 / Android 连续返回增加 pending history 队列；转场期间产生的新 `popstate` 会在当前动画结束后追到最终历史状态。
- bfcache / 系统返回恢复时主动清理遗留 `is-busy`、veil、flash 状态，降低整页突然无法点击的风险。
- 地球与国家地图在触控设备上提高“点击 vs 拖动”判定阈值，降低手指拖动造成误进入国家 / 地区。
- 手机导航、菜单与通用按钮扩大最低触控尺寸。

### Reliability
- Private Storage Signed URL 增加失败后的自动补签与去重机制。
- 增加 `SB.store.health()` 轻量诊断接口，便于周年版实测定位 Database / Storage 权限问题。


### Fixed
- **Auth recovery hotfix:** 登录错误状态不再统一落入“重新连接”死路。密码/凭据错误保持在登录表单内提示；无 Book 权限和 RLS/数据库访问异常增加“返回登录”出口。
- “返回登录”会退出当前 Supabase Session、清空当前 Book Context 并回到登录表单，无需刷新页面。
- **Phase 2 interaction hotfix:** 修复 Runtime Book Context 与 V1 魔法书视觉控制器同时使用 `SB.book` 导致的全局命名覆盖。现在 `SB.book` 仅表示当前数据 Book，魔法书封面/开书动画改为 `SB.magicBook`。
- 修复该冲突引发的 Store 无法稳定取得 `book_id / role`、登录后场景交互异常风险。
- 修正 Anniversary Bridge SQL：移除周年版非必要的自定义 helper function，改用直接 RLS membership 判断，降低迁移兼容风险。
