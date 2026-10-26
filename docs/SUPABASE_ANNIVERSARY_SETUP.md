# Supabase Anniversary Setup

## 已写入前端的公开配置

项目已配置：
- Project URL: `https://xowbbcumcxtsrrnulunb.supabase.co`
- Publishable Key: 已写入 `blocks/00-config.html`

Publishable Key 是浏览器客户端密钥；不要把 Secret Key、service_role、数据库密码写入项目。

## 你现在需要做的操作

### 1. 确认 Owner Auth User 存在
Supabase Dashboard → Authentication → Users。

Owner UID 应为：
`d5aa2cab-0d61-4cda-8ca8-1299a1c49693`

如果这个 UID 对应你的实际登录账户，继续下一步。

### 2. 运行数据库 Migration
Dashboard → SQL Editor → New query。

复制并运行：
`supabase/migrations/001_anniversary_bridge.sql`

运行成功后，应出现：
- public.books
- public.book_members
- public.book_data
- Storage bucket `starbook-media`

### 3. 初始化周年 Book
继续在 SQL Editor 运行：
`supabase/seed/002_anniversary_owner.sql`

它会创建固定 Book：
- Book ID: `8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`
- Name: `星屿之书`
- relationship: romantic
- theme: magic-celestial
- experience: world-map
- 你的角色: owner

脚本可重复运行，不会清空已有 `book_data`。

### 4. 检查 Storage
Dashboard → Storage。

确认：
- `starbook-media` 存在
- Public = OFF

不要把 Bucket 改成 Public。

### 5. 本地/Pages 登录测试
重新运行：

```bash
python build.py
```

通过 HTTP 服务器打开，而不是直接双击 `file://`：

```bash
python -m http.server 8000 -d site
```

浏览器访问 `http://localhost:8000`。

使用你的 Supabase Email + Password 登录。

成功后应自动打开唯一一本《星屿之书》。

### 6. 测试数据写入
依次验证：
- 新增城市
- 新增一段回忆
- 上传一张照片
- 刷新网页后仍存在
- 修改回忆
- 删除回忆

### 7. 验证 Private Storage
上传图片后，在 Dashboard → Storage 中应该看到类似：

```text
8a3cc6fe-b667-4ce7-b47b-79cebc0e1353/images/xxxx.jpg
```

Bucket 仍必须是 Private。

### 8. v1.5.1 标题与成员 migration

当前项目在 v1.5.1 使用：

`supabase/migrations/002_v151_title_and_members.sql`

该 migration 会：

- 将当前 Book 标题统一为《星屿之书》；
- 添加 editor `11aa32fe-3875-4880-81fb-02a543dca853`；
- 添加 editor `62adee54-c59a-4844-abb5-1b5629da3bf9`。

运行前确认两个 UID 已存在于 Authentication → Users。脚本不会修改回忆 payload 或 Storage。

`003_add_partner_template.sql` 保留作为未来手动追加单个成员的通用模板。

## 若运行 SQL 报错
不要关闭 RLS 来绕过错误。

保留完整错误文本，再根据错误修 migration/policy。
