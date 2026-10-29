# Starbook 导入参考（基于本地 v1.9.2）

城市在国家地图中选择省/州后添加：`country`, `countryName`, `region`, `regionName`, `name`, `lon`, `lat`。页面的添加逻辑使用行政区中心坐标；相同 region 和 name 不可重复。确认真实国家及行政区并使用页面实际选项。

回忆编辑器保存 `cityId`, `title`, `date`（YYYY-MM）, `note`, `slides`, `cover`, `bgmMode`, `bgm`, `style`, `season`；照片上传后产生 `{id,w,h}`，slide 带 `caption` 和可选 `g`；`groups` 是 `{id,text}` 的数组，组内成员必须连续。标题最多 40，导入语最多 300，照片描述最多 120，组描述最多 300；均按 HTML maxlength 的 UTF-16 代码单元计算。编辑器年份选项从 2000 到当前年份加一，必须确认网页可表达所需日期。至少一张照片。网页选择两张以上创建分组，组内描述放映时使用组描述。风格、季节、音乐根据 [创作 prompt](creative-prompt.md) 选择。

浏览器 `SB.store.uploadImage` 将图片最长边限制为 2400 像素，转为 JPEG（质量 .86），上传到当前 Book 的 private storage；`saveMemory` 使用 revision 冲突检测。图片是私有数据。任何失败需核实结果再继续，避免未引用对象和重复回忆；不要绕过正常权限或直接替换整本书数据。

本版本未发现正式素材包导入 UI。素材包旧说明中引用的 `docs/AGENT_PHOTO_IMPORTER.md` 和 `tools/agent-importer/README_AGENT.md` 在考察的仓库中不存在；不要假定其可用。

扫描清单为本 skill 的中间格式，不是网页原生导入文件：每个 event 的 `city`, `country`, `region`, `source_date`, `date`, `title`, `note`, `cover_file` 及每个图片的 `caption`, `group` 由 agent 填写；`groups` 为 `{id,text}` 列表。`file` 相对于事件目录，`sha256` 是原文件哈希。`status` 必须在完成看图、写作、核实后改为 `ready`。保留 `issues` 说明未解决情况。原故事与素材只读；既有 `放映文案.md` 可供参考，`memory.agent.json` 或旧计划可能过期。
