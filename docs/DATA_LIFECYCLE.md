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

- Book JSON 导出；
- Metadata 导出；
- Storage asset manifest；
- 恢复流程。

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
