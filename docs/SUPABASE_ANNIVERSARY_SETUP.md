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
- private schema helper functions
- Storage bucket `starbook-media`

### 3. 初始化周年 Book
继续在 SQL Editor 运行：
`supabase/seed/002_anniversary_owner.sql`

它会创建固定 Book：
- Book ID: `8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`
- Name: `我们的星屿`
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

成功后应自动打开唯一一本《我们的星屿》。

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

### 8. 女朋友账号之后再添加
创建她的 Auth User 后，复制她的 User UUID。

打开：
`supabase/seed/003_add_partner_template.sql`

把：
`YOUR_PARTNER_USER_UUID`

替换成实际 UUID 后运行。

她将获得 `editor` 权限。

不要提供她的密码给任何代码或 AI。

## 若运行 SQL 报错
不要关闭 RLS 来绕过错误。

保留完整错误文本，再根据错误修 migration/policy。
