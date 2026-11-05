# Starbook Data Lifecycle & Migration Policy

## 1. 核心原则

Starbook 的真实用户数据与前端代码版本分离。

```text
GitHub / Pages = Code Lifecycle
Supabase = User Data Lifecycle
```

因此：

> 发布新代码版本，不应该要求用户重新导入旧数据。

## 2. 当前 Production 数据位置

### Supabase Auth

保存用户身份与 Session。

### Database

当前 Anniversary Bridge：

- `books`
- `book_members`
- `book_data`

### Private Storage

Bucket：

```text
starbook-media
```

当前路径：

```text
{book_id}/images/...
{book_id}/audio/...
```

## 3. 当前 Book 数据格式

`book_data.payload`：

```json
{
  "cities": {},
  "memories": {},
  "settings": {}
}
```

`schema_version` 当前为 Bridge 数据版本。

### Memory 可选表现字段（v1.7.0）

`memories[id]` 在原有字段之外可以有：

- `style`：放映风格 `cinema | constellation | journal`，缺省视为 `cinema`；
- `season`：季节主题 `auto | none | spring | summer | autumn | winter`，缺省视为 `auto`。
- `groups`（v1.9.1）：`[{id, text}]`，照片分组「同一时刻」的共同描述；照片 `slides[k].g` 为所属组 id。均为可选字段，缺省 = 没有分组；组成员在 `slides` 中连续；只保存仍有成员的组。

它们是当前 Theme（`magic-celestial`）的**表现偏好**，不是业务数据：只在用户编辑并保存回忆时写入，旧数据无需迁移，`schema_version` 不变；其他 Theme 可以忽略。未来正规化 Memory 表时，应作为可空的 presentation 列或 JSON 偏好保留。

`revision` 用于轻量并发覆盖检测。

## 4. 普通前端版本升级

例如：

```text
1.5.1 → 1.5.2
```

如果只是 UI / JS / 稳定性 / 文档：

- 不运行 production SQL；
- 不重新创建 Book；
- 不运行 owner seed；
- 不重新上传图片；
- 不清空 Storage；
- 不改 schema_version。

新版前端继续读取同一个 Book ID 和 Supabase 数据。

## 5. Seed 与 Migration 的区别

### Seed

用于第一次创建初始实例。

例如：

- `002_anniversary_owner.sql`

它不是每版部署脚本。

### Migration

用于已有 production 数据上的结构升级。

未来例如：

```text
002_add_profiles.sql
003_add_assets.sql
004_normalize_memories.sql
```

Migration 应该将旧数据**向前转换**。

## 6. 禁止的数据操作

未经明确备份和用户批准，不允许：

- `drop table` production 核心表；
- `truncate` production 数据；
- 清空 `book_data.payload`；
- 删除整个 Private Bucket；
- 重新 seed 覆盖真实回忆；
- 因为前端 Bug 重置数据库；
- 把 Private Bucket 改成 Public。

## 7. 未来正规化策略

目标：

```text
book_data.payload
        ↓ migration
memories
locations
assets
settings
tags
...
```

迁移原则：

1. 新表先建立；
2. 从 JSONB 读取并迁移；
3. 双读/验证（如果必要）；
4. 验证数量和关键字段；
5. 切换 Store；
6. 保留可恢复路径；
7. 最后才考虑废弃旧字段。

## 8. schema_version

任何会改变生产数据语义的迁移都应考虑更新 schema version。

前端如果要求更高 schema，应：

- 给出明确错误/升级提示；
- 不静默破坏旧数据；
- 不自动执行不可逆生产 migration。

## 9. 数据备份

周年后 P1 应实现：

- Book JSON 导出；（v1.12.0 已实现：「导出整本书」，含照片原图与文件清单）
- Metadata 导出；（v1.12.0：`book.json` 含书名、导出时间、统计）
- Storage asset manifest；（v1.12.0：`book.json.files` + 每卷清单）
- 恢复流程。（v1.12.1 已实现：「从备份导入」）

在此之前，重要 schema migration 前至少应有 Supabase 侧备份/导出策略。

## 10. 删除 Book 的未来规则

未来多 Book 平台中，“删除 Book”应是明确产品动作，并处理：

- membership；
- memories；
- assets；
- Storage；
- retention / soft delete；
- owner confirmation。

当前周年版本不实现 Book 删除，避免误删真实数据。


## 非破坏性成员 / 元信息 Migration 示例

`v1.5.1` 使用 `supabase/migrations/002_v151_title_and_members.sql` 更新 Book 标题并 upsert Book Members。该 migration 不修改 `book_data.payload`、不删除 Storage，是“代码版本升级不重置真实数据”的标准示例。

## v1.10.1 可选字段扩展（无 migration）

- 回忆 `date`：在原有 `YYYY-MM` 之外允许 `YYYY-MM-DD`（编辑器新增「日」）。旧数据保持原样，前端按当月 1 日排序；不需要、也不允许批量改写旧数据。
- `settings.anniversary`：可选 `YYYY-MM-DD`；在时光长卷「纪念日」徽记里设置 / 恢复默认（写 `null`）。
- 两者都在 `book_data.payload` 内，通过现有 `SB.store.saveMemory / saveSettings` 写入（乐观锁 revision 不变），无 SQL、无 schema 变化；回滚到 v1.10.0 时旧前端会把 `YYYY-MM-DD` 当作年月读取（显示到月），不会丢数据。

## v1.12.0 回收站（软删除）与导出备份（无 migration）

- 新可选字段 `book_data.payload.trash = {memories, cities, photos, files}`（结构见 `prompts/16-archive.md`）。删除回忆 / 城市、在编辑器移除照片、替换音乐，都先进入回收站保留 30 天；期间 Storage 文件**不删除**。
- 只有「彻底删除」「清空最近删除」或编辑者载入时的过期清理（超过 30 天）才删除 Storage 文件（`mutate(fn, {purge:true})`）。
- Supabase 为 **Free 套餐，没有自动备份**；付费套餐的数据库备份也不包含 Storage 文件。因此 v1.12.0 提供「导出整本书」：`book.json`（完整 payload，含回收站）+ 照片原图 + 音乐，按卷打包下载到本机。建议每季度导出一次，电脑与网盘各存一份。
- 回滚到 v1.11.x 时：旧前端不认识 `trash`，下一次保存会丢掉回收站记录（文件不会被删除，但无法再从界面恢复）；回收站中的照片文件会成为孤立文件，不影响任何功能。
- v1.12.1 起可「从备份导入」：只新增 / 可选覆盖，不删除现有数据；照片按原路径补传（已存在跳过）。

## v1.12.1 从备份导入（无 migration）

- 导入是**加法**：缺少的城市 / 回忆新增，已存在的默认保留（可选覆盖），从不删除任何现有回忆、城市或文件。覆盖时被替换掉的照片按 v1.12.0 规则进入回收站。
- 媒体：先用 `createSignedUrls` 判断哪些文件已存在，只上传缺少的，上传到导出时记录的原路径（同一本书）或改写到当前书的前缀（另一本书的备份）；`upsert:false`，不覆盖已有文件。
- 写入：媒体上传完成后一次 `mutate`（revision 乐观锁）；中途取消或部分失败时，已上传的文件保留，可以再次导入补齐。
- 备份格式见 `prompts/16-archive.md` 6.1；`formatVersion` 只能向前兼容地递增。

## v1.12.2 城市真实位置（无 migration）

- City 的 `lon / lat` 从 v1.12.2 起尽量保存真实位置（添加时选候选，或在编辑里「校准位置」）。旧城市**不自动迁移**，坐标保持原样，可由编辑者逐个校准。
- 校准到另一个地区时同时改写 `region / regionName`；回忆仍按 `cityId` 关联，不受影响。
- 位置候选的在线查询只发送「城市名 + 国家代码」到 Open-Meteo，不发送任何回忆数据。

