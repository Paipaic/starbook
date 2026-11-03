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
