-- Starbook v1.5 Anniversary Book 初始化
-- 前提：先执行 migrations/001_anniversary_bridge.sql
-- Owner UID 已按当前项目填写。

begin;

insert into public.books (
  id,name,relationship_type,theme_id,experience_id,created_by
) values (
  '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353',
  '我们的星屿',
  'romantic',
  'magic-celestial',
  'world-map',
  'd5aa2cab-0d61-4cda-8ca8-1299a1c49693'
)
on conflict (id) do update set
  name = excluded.name,
  relationship_type = excluded.relationship_type,
  theme_id = excluded.theme_id,
  experience_id = excluded.experience_id,
  updated_at = now();

insert into public.book_members (book_id,user_id,role,status)
values (
  '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353',
  'd5aa2cab-0d61-4cda-8ca8-1299a1c49693',
  'owner',
  'active'
)
on conflict (book_id,user_id) do update set role='owner',status='active';

insert into public.book_data (book_id,schema_version,payload,revision)
values (
  '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353',
  1,
  '{"cities":{},"memories":{},"settings":{}}'::jsonb,
  0
)
on conflict (book_id) do nothing;

commit;
