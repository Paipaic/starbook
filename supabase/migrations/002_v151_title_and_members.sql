-- Starbook v1.5.1
-- 非破坏性向前 migration：统一当前 Book 标题，并加入两名 editor。
-- 本脚本不会修改 book_data.payload，不会删除/重建 Storage，也不会重新 seed 回忆数据。
-- 可重复执行。

begin;

-- 1) 统一当前 Anniversary Book 的展示标题。
update public.books
set name = '星屿之书',
    updated_at = now()
where id = '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353';

-- 2) 加入两名 editor。
-- 通过 auth.users 做来源校验：只有 UID 已真实存在于 Supabase Auth 时才插入。
insert into public.book_members (book_id, user_id, role, status)
select
  '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353'::uuid,
  u.id,
  'editor',
  'active'
from auth.users u
where u.id in (
  '11aa32fe-3875-4880-81fb-02a543dca853'::uuid,
  '62adee54-c59a-4844-abb5-1b5629da3bf9'::uuid
)
on conflict (book_id, user_id)
do update set
  role = 'editor',
  status = 'active';

-- 3) 如果两个 UID 任意一个不存在，主动中止并回滚，避免“看起来成功但成员没加全”。
do $$
declare
  expected_count integer := 2;
  actual_count integer;
begin
  select count(*) into actual_count
  from public.book_members
  where book_id = '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353'::uuid
    and user_id in (
      '11aa32fe-3875-4880-81fb-02a543dca853'::uuid,
      '62adee54-c59a-4844-abb5-1b5629da3bf9'::uuid
    )
    and role = 'editor'
    and status = 'active';

  if actual_count <> expected_count then
    raise exception 'v1.5.1 membership migration incomplete: expected % editor members, found %. Confirm both UID values exist in Authentication > Users.', expected_count, actual_count;
  end if;
end $$;

commit;

-- 可选验证查询：运行 migration 后可单独执行查看结果。
-- select b.name, bm.user_id, bm.role, bm.status
-- from public.books b
-- join public.book_members bm on bm.book_id = b.id
-- where b.id = '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353'
-- order by bm.role, bm.user_id;
