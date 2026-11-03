# 块 16 · 珍藏与备份：最近删除 + 导出整本书（v1.12.0）

> 规划条目 #1（回收站）、#2（导出整本书）。背景：Supabase 为 Free 套餐，没有任何自动备份；即使付费套餐的备份也不含 Storage 照片。v1.11.1 及以前删除回忆 / 城市、在编辑器里移除照片、替换音乐，都会在保存成功后**立即永久删除** Storage 文件。
>
> 参考资料：JSZip `generateAsync`（`type:'blob'`、`compression:'STORE'` 不压缩 JPEG、`onUpdate` 进度；默认把每个文件和结果都放在内存里——大书必须分卷）；JSZip Limitations（结果整体在内存中、ZIP64 大小限制）；Chrome 对「连续自动下载多个文件」会询问权限（第 2 卷起必须由用户点击触发）；软删除（soft delete + 定期清理）通行做法。

## 1. 数据结构（`book_data.payload` 内，无 schema 变化）

```json
"trash": {
  "memories": { "<memoryId>": { ...回忆全部字段, "deletedAt": "ISO", "viaCity": "<cityId>|undefined" } },
  "cities":   { "<cityId>":   { ...城市全部字段, "deletedAt": "ISO" } },
  "photos":   { "<path>":     { "slide": {...}, "memoryId": "...", "memoryTitle": "...", "deletedAt": "ISO" } },
  "files":    { "<path>":     { "deletedAt": "ISO" } }
}
```

- `normalize()` 必须保留 `trash`（缺省为四个空对象）；`refs()` 把回收站里的回忆媒体、照片、`files` 都算作「仍被引用」。
- **通用兜底**：`mutate()` 写入前，凡是「之前被引用、现在不再被引用」的文件，一律记入 `trash.files`（30 天后清理），不再立即删除。只有 `mutate(fn, {purge:true})`（彻底删除 / 过期清理）才会真正删除 Storage 文件。
- 从未保存过的上传（编辑器里上传后又取消）仍由 `deleteFile` 立即删除——它们不在任何 payload 里。

## 2. Store API（`blocks/05-store.html`）
- `removeMemory(id)`：回忆移入 `trash.memories`。
- `removeCity(id)`：城市移入 `trash.cities`，它的全部回忆移入 `trash.memories`（`viaCity = id`）。
- `saveMemory(m)`：与旧版本比较，被移除的照片记入 `trash.photos`（含 slide 原数据，用于恢复）。
- `restoreMemory(id)`：所在城市在回收站 → 一并恢复城市；城市已彻底删除 → 报错「所在的城市已经彻底删除」。
- `restoreCity(id)`：同省已有同名城市（删除后又重新添加过）→ 回忆并入现有城市，不再恢复重复城市；否则恢复城市。随后恢复 `viaCity = id` 的回忆。
- `restorePhoto(path)`：所在回忆必须存在（否则提示先恢复回忆）；照片追加到该回忆末尾，去掉分组标记（保持分组连续性规则）。
- `purgeTrash({kind, id} | 'expired' | 'all')`：彻底删除。删城市连带删它在回收站中的回忆；删回忆连带删它在回收站中的照片。
- `st.trash`（只读视图）、`st.trashCount()`、`TRASH_DAYS = 30`。
- 编辑者每次载入后，若有超过 30 天的条目，自动静默清理一次。

## 3. 界面（`blocks/16-archive.html`）
- 右上角标识新增「珍藏与备份」（在动效与账户之间）。小面板：
  - 「最近删除 · N 项」（编辑者）→ 打开对话框；
  - 「导出整本书」→ 打开导出对话框；显示「上次导出：日期」（本机记录）。
- 「最近删除」对话框：按「城市 / 回忆 / 照片」分组；每项显示名称、所在位置 / 日期 / 照片数、「还剩 N 天」；操作「恢复」「彻底删除」（二次确认）；底部「清空最近删除」（二次确认，危险按钮）；替换掉的音乐等文件只显示数量说明。空状态：「最近删除是空的。删除的回忆、城市和照片会在这里保留 30 天。」
- 所有删除确认文案改为「移到最近删除，30 天内可在右上角『珍藏与备份』里恢复」。

## 4. 导出整本书
- 所有成员可用（只读取）。建议在电脑上导出（对话框里说明）。
- 内容：`book.json`（格式标记 `starbook-export`、版本、导出时间、书名、完整 payload 含回收站、文件清单）、`README.txt`（中文说明：如何查看、文件夹结构、分卷说明）、`images/`、`audio/`。
- 下载：`SB.supabase.storage.from(bucket).download(path)`，并发 3，单个文件失败重试 2 次；失败的文件列入 `导出失败的文件.txt`。
- 分卷：每卷上限 电脑 400MB / 手机 150MB；`compression:'STORE'`。第 1 卷生成后自动保存；第 2 卷起显示「保存第 k 卷」按钮，由用户点击保存（避免浏览器拦截连续下载）。每卷附 `清单-第k卷.txt`。
- 进度：已下载 x / y 个文件、已打包大小；可随时取消（已保存的分卷保留）。
- JSZip 只在导出时加载，锁定版本 `3.10.1`（cdnjs，jsDelivr 后备）。

## 5. 验收
- 删回忆 → Storage 未删除 → 在最近删除里恢复 → 放映正常。
- 删城市（含 2 段回忆）→ 地球 / 面板中消失 → 恢复后城市与回忆都回来。
- 编辑回忆移除 2 张照片并保存 → 最近删除出现 2 张照片 → 恢复后照片回到回忆末尾。
- 彻底删除 / 清空 / 过期清理 → 才调用 Storage remove。
- 查看者看不到「最近删除」，可以导出。
- 导出：zip 中照片数量与书中一致；`book.json` 可被 JSON 解析。

## 6. v1.12.1 · 从备份导入（与导出格式一一对应）

> Owner 需求：补充「重新导入」，导出的文件与格式要和导入对应，照片、地点、时间、编组等各项设置关系都要对应上。
> 参考资料：JSZip `loadAsync`（读取中央目录，文件内容按需 `file.async('blob')` 解出）；Supabase Storage `createSignedUrls`（批量；对象不存在时该条返回 `error`）与 `upload(path, blob, {upsert:false})`（已存在返回 Duplicate / 409）。

### 6.1 导出格式 `starbook-export` v1（导出与导入的唯一契约）
- 第 1 卷：`book.json`、`README.txt`、`清单-第1卷.txt`、媒体文件；第 k 卷：`清单-第k卷.txt` + 媒体文件；最后一卷可能有 `导出失败的文件.txt`。
- `book.json`：
  - `format: "starbook-export"`、`formatVersion: 1`、`app`、`exportedAt`、`book: {id, name}`、`counts`；
  - `files: [{path, file}]`——**原 Storage 路径 ↔ zip 内文件名**（`images/<id>.jpg` / `audio/<id>.<ext>`）；导入时按这张表把每个 zip 文件放回原路径；
  - `payload`：导出时完整的 `book_data.payload`（`cities / memories / settings / trash`），原样保存，不做任何转换。回忆的照片顺序、照片说明、分组（`groups` + `slides[k].g`）、封面、日期（`YYYY / YYYY-MM / YYYY-MM-DD`）、所在城市（`cityId` → `cities[id]` 的国家 / 省份 / 经纬度）、放映风格 / 季节 / 音乐设置、纪念日，全部在 payload 里。
- 新版本只能在 `book.json` 里**增加**字段；不改已有字段的含义。导入遇到 `formatVersion > 1` 时提示「这是更新版本的备份，请先更新网站」。

### 6.2 导入流程（编辑者；在「珍藏与备份」里）
1. 选择 zip（可多选，分卷备份请一次选中全部分卷）。在浏览器本地读取，不上传 zip 本身。
2. 校验：必须找到 `book.json` 且 `format` 正确；按 `files` 表统计已选分卷里缺少的文件（缺第 1 卷 → 提示「请同时选中第 1 卷」）。
3. 预览：备份时间、书名、城市 / 回忆 / 照片数；将「新增 a 座城市、b 段回忆」「c 段回忆这本书里已经有了」「d 个照片文件需要上传」「缺少 e 个文件」。选项：「已存在的回忆用备份里的版本覆盖」（默认关闭 = 保留现在的版本）。
4. 导入：
   - 先检查哪些照片 / 音乐在 Storage 里已经存在（`createSignedUrls` 批量，100 个一批）；只上传缺失的（并发 2，失败重试 2 次），**上传到原路径**（同一本书）；
   - 备份来自另一本书（`book.id` 不同）时，路径前缀换成当前书的 id，payload 中所有媒体引用同步改写；
   - 媒体上传完成后**一次** `mutate` 合并数据（乐观锁、可重试）。
5. 合并规则（`SB.store.importBackup(payload, {overwrite, remap})`）：
   - 城市：同 id 已存在 → 保留（覆盖模式下用备份版本）；同 id 不存在但同国家 + 省份 + 名称的城市已存在 → 回忆并入该城市；否则新增。若该 id 在「最近删除」里 → 从回收站移除后按新增处理。
   - 回忆：同 id 已存在 → 保留 / 覆盖；否则新增（`cityId` 按上一步的并入关系改写）。回忆对象整体复制，照片顺序、说明、分组、封面、日期、风格、季节、音乐全部保留。若该 id 在「最近删除」里 → 从回收站移除后新增。
   - 设置：当前没有纪念日 / 全站音乐时才用备份的值。
   - 回收站：备份里的回收站条目，当前书中既没有同 id 的正常条目也没有回收站条目时才加入，`deletedAt` 保持原值。
6. 结果：新增 / 覆盖 / 保留 / 跳过的数量；上传失败或缺失的文件列表（可再次导入补齐——已存在的文件不会重复上传）。
