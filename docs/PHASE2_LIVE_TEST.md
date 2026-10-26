# Starbook v1.5 · Phase 2 实机验证清单

> 目标：在增加周年献词/彩蛋之前，先证明 Auth → Book → JSONB → Private Storage 的完整链路可靠。

## 0. 已确认

- `001_anniversary_bridge.sql` 已成功执行。
- `002_anniversary_owner.sql` 已成功执行。
- 《我们的星屿》Seed 查询返回 1 行。
- `starbook-media` 已确认 `public = false`。

## 1. 本地启动

在项目根目录运行：

```bash
python build.py
python -m http.server 8000 -d site
```

浏览器打开：

```text
http://localhost:8000
```

不要用 `file://` 双击测试周年版。

## 2. 登录测试

使用 owner 账号的 Email + Password 登录。

通过标准：

- 能看到星屿风格登录门。
- 正确密码可以进入。
- 错误密码显示友好提示。
- 进入后仍是原来的魔法书体验，而不是管理后台。
- 刷新后 Session 能恢复，不要求再次输入密码。

## 3. Console 快速诊断

进入 Starbook 后打开浏览器 DevTools → Console，运行：

```js
await SB.store.health()
```

预期关键字段：

```js
{
  connected: true,
  role: "owner",
  canEdit: true,
  database: true,
  storage: true
}
```

如果某项为 false，请保留整个返回对象和 Console 红色报错。

## 4. 最小数据写入测试

只创建测试内容，不要立即大量导入周年正式照片。

1. 新增一座测试城市。
2. 新增一段测试回忆。
3. 上传 1 张 JPG/PNG。
4. 保存。
5. 刷新页面。
6. 确认城市、回忆和照片仍然存在。
7. 修改标题或描述，再保存。
8. 再次刷新确认修改存在。

## 5. Private Storage 测试

通过标准：

- 上传照片后能立即预览。
- 刷新页面后照片仍能显示（说明 Signed URL 能重新生成）。
- Supabase Storage 中对象路径以当前 `book_id` 开头。
- Bucket 仍为 Private。
- 删除测试回忆后，不再使用的媒体最终可以被清理。

## 6. 音乐测试

1. 上传 1 个小型 MP3 或 M4A（建议先小于 5 MB）。
2. 保存为回忆专属 BGM 或全站 BGM。
3. 试听。
4. 刷新页面后再次播放。

## 7. 返回键测试

按以下路径逐层进入：

```text
魔法书 → 地球 → 大洲 → 国家 → 地区/城市
```

然后连续使用浏览器 Back。

通过标准：

- 应逐层返回 Starbook 上一场景。
- 不应第一下就退出网站。
- 页面自己的返回按钮与浏览器 Back 都能使用。

## 8. 手机测试

至少在周年当天实际使用的手机上测试：

- 登录输入框不被键盘遮挡。
- 地图可触控。
- 回忆弹窗能滚动。
- 图片上传能从相册选择。
- BGM 能播放。
- 系统返回键/浏览器返回行为正常。

## 9. 发生错误时需要保留的信息

如果失败，不要关闭 RLS，也不要把 Bucket 改成 Public。

请记录：

1. 哪一步失败。
2. 页面显示的提示。
3. DevTools Console 红色错误。
4. `await SB.store.health()` 的完整结果（如果已经成功登录）。

不要提供密码、Secret Key、service_role 或数据库密码。
