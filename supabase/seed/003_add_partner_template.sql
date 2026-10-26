-- 女朋友账号创建后使用。
-- 只替换下面 YOUR_PARTNER_USER_UUID；不要填写密码。

insert into public.book_members (book_id,user_id,role,status)
values (
  '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353',
  'YOUR_PARTNER_USER_UUID'::uuid,
  'editor',
  'active'
)
on conflict (book_id,user_id) do update set role='editor',status='active';
