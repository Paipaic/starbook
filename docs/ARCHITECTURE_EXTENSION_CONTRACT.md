# Starbook Architecture & Extension Contract

> 本文定义 Starbook 当前架构中**不能被后续优化无意破坏**的长期扩展契约。

## 1. 平台长期模型

Starbook 长期抽象：

```text
User
  ↕
Book Membership
  ↕
Book
├─ Relationship Type
├─ Theme
├─ Experience
├─ Memories
├─ Assets
├─ Locations
└─ Settings
```

当前只实现其中一个受限实例：

```text
relationship = romantic
theme = magic-celestial
experience = world-map
```

但 Core 不得把这三个值视为唯一可能。

## 2. User 与 Book

必须保持：

- 一个 User 可加入多本 Book；
- 一本 Book 可有多个 User；
- User 与 Book 是多对多；
- `book_members` 是权限关系来源；
- Book 内容属于 Book，不属于单个 User。

禁止：

```text
user_id == book_id
一个账户 == 一本书
照片归用户目录而非 Book
```

## 3. Runtime namespaces

### `SB.user`

职责：

- Supabase session；
- 当前 user；
- auth state。

### `SB.book`

职责：

- 当前数据 Book；
- 当前 membership role；
- Book metadata。

不得负责视觉魔法书。

### `SB.magicBook`

职责：

- Magic Celestial Theme 的书封面；
- 宝石；
- 悬浮；
- 开书视觉动画。

它是 Theme-specific controller，不是业务 Book Context。

### `SB.gate`（v1.8.0）

Magic Celestial Theme 的转场视觉（门钥匙 / 幻影显形 / 熄灯器）。

- 只提供 cover / reveal / portal 装饰，**不拥有场景生命周期**；Scene Runtime 仍负责 `prepare → cover → await enter → nextPaint → reveal`。
- 属于 Theme 层：未来其他 Theme 可提供自己的 `SB.gate` 实现；缺失时 Scene Runtime 回退到通用 veil / flash。
- 不读写任何业务数据。

### `SB.globe` 搜索（v1.8.0）

World Map Experience 的地球搜索：离线 `SB.WORLD_CITIES` + Open-Meteo 在线城市搜索。

- 外部请求只包含用户输入的搜索词，不发送 Book / Memory / 照片 / 账户数据；
- 在线服务不可用不影响任何核心链路（降级为离线库）；
- 搜索结果只用于转动地球与导航，不写入 Store。

### `SB.editor.photoActions`（v1.9.0）

回忆编辑器「影像管理台」的批量操作注册表：`{id, label, icon, danger?, when(sel, st), run(sel, ctx)}`。只修改编辑中的 `st.slides` / `st.cover` / `st.groups`，不直接读写 Store；保存、文件清理仍由编辑器统一完成。新增批量能力时追加注册项即可。

v1.9.1：`label` 可以是函数 `label(sel, st)`（例如「编为一组 / 加入这一组 / 合并为一组」）；改变照片顺序的操作结束前必须调用编辑器的分组规范化（组成员保持连续），撤销快照用 `snapOf(st)`（含每张照片的组与组描述）。

### `SB.theme`

当前只有 Context：

```text
magic-celestial
```

未来可升级 Theme registry / loader，但当前不要过度实现。

### `SB.experience`

当前：

```text
world-map
```

未来可以：timeline / family-tree / album / constellation 等。

### `SB.store`

当前业务兼容层。

原则：

- 地图、编辑器、播放器尽量通过 Store API 访问业务数据；
- 不要让每个业务模块直接散落 Supabase 查询；
- 未来正规化数据库时，优先换 Store 内部实现，降低 UI 重写成本。

## 4. Relationship 与 Theme 解耦

合法组合示例：

```text
romantic + magic-celestial
romantic + vintage-album
friendship + magic-celestial
family + forest-grimoire
```

关系类型可以推荐 Theme，但不能决定 Theme。

## 5. Theme 与 Experience 解耦

Theme = 长什么样。

Experience = 怎么探索。

当前：

```text
Magic Celestial + World Map
```

未来同一个 Theme 可以承载不同 Experience；同一个 Experience 也可被不同 Theme 皮肤呈现。

## 6. Memory First 的未来方向

当前 V1 遗留结构是：

```text
City → Memory
```

长期应演进为：

```text
Book
 ↓
Memory
├─ optional Location
├─ Assets
├─ Date
├─ Tags
├─ People
└─ Text
```

地图只是根据 Location 展示 Memory 的一种 Experience。

因此后续新功能禁止进一步制造：

```text
Memory 必须有 City
```

这样的强依赖。

## 7. Storage 所属原则

路径以 Book 为第一层：

```text
{book_id}/images/...
{book_id}/audio/...
```

原因：

- 资源属于 Book；
- 成员变化不应改变资产归属；
- RLS 以 Book membership 判断权限；
- 未来导出/删除一本 Book 更清晰。

## 8. 当前 Anniversary Bridge 是兼容层

当前：

```text
book_data.payload
```

保存 V1 JSON。

它不是最终 V2 schema。

任何 Agent 不应因为“JSONB 已经能用”而把未来所有新平台功能继续无限塞入同一个大 JSON。

周年后应逐步正规化。

## 9. Theme / Experience 当前不做什么

在周年版阶段：

- 不实现动态插件商城；
- 不引入复杂框架；
- 不拆完所有 Theme 组件；
- 只保持正确 Context 和代码边界。

## 10. 扩展兼容检查

每次新增功能至少问：

- 如果用户有 2 本 Book，还成立吗？
- 如果 Book 是 family 而不是 romantic，还成立吗？
- 如果 Theme 不是 magic-celestial，还成立吗？
- 如果 Experience 不是 world-map，还成立吗？
- 如果 Memory 没有 Location，还成立吗？
- 如果当前用户只是 viewer，还成立吗？

如果答案是否定的，需要明确说明“这是当前 Theme/Experience 特有能力”，而不是把限制写进 Core。

### `SB.yearReel`（v1.10.0）

「时光剪影」周年回放：`open({year, from:'YYYY-MM-DD', to:'YYYY-MM-DD'|null（不含当天）, list:[memory…], now})`（v1.10.1 起精确到日，仍兼容 `YYYY-MM`） / `close()`。只读回忆数据，不写入 Store；由时光长卷的周年节点调用。新的回顾类放映（例如「每月剪影」）可以复用同一接口传入不同的 `list` 与区间。

### `SB.overview`（v1.10.0，调试）

`state`（站点数、焦点、纪念日起点、节点列表）、`center(i)`（v1.10.1 起为定时缓动直达）与 `hitPoint(i)`；只用于测试与外部跳转，不要在其中加入业务逻辑。

### `SB.date`（v1.10.1）

Core 级日期工具（`blocks/00-core.html`）：`parse / day / str / dot / addYears / daysIn / valid / hasDay / today`。回忆日期允许 `YYYY` / `YYYY-MM` / `YYYY-MM-DD`；排序、周年、分段必须使用 `SB.date.day()`。它不含任何关系 / 主题语义，未来其他 Experience 可直接复用。

### `settings.anniversary`（v1.10.1）

Book 级可选设置（`book_data.payload.settings.anniversary`，`YYYY-MM-DD`），表示这本书的「周年起点」。当前只有时光长卷使用；名称不绑定「情侣」语义——其他关系的书也可以把它理解为「这本书的纪念日」。未设置时由 Experience 自行决定默认值（当前：最早一段回忆的日期）。
