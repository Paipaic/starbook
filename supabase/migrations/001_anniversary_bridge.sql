-- Starbook v1.5.0-anniversary
-- Anniversary Bridge Architecture (function-free migration)
-- 在 Supabase Dashboard -> SQL Editor 中“整段运行”。
-- 本文件不需要、也不应包含 Secret Key / service_role / 数据库密码。
-- 设计目标：截止周年交付前，优先减少迁移脚本复杂度与兼容风险。

begin;

create extension if not exists pgcrypto;

create table if not exists public.books (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  relationship_type text not null default 'romantic',
  theme_id text not null default 'magic-celestial',
  experience_id text not null default 'world-map',
  created_by uuid not null references auth.users(id) on delete restrict,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.book_members (
  book_id uuid not null references public.books(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null default 'viewer' check (role in ('owner','editor','viewer')),
  status text not null default 'active' check (status in ('invited','active','left','removed')),
  created_at timestamptz not null default now(),
  primary key (book_id,user_id)
);

create table if not exists public.book_data (
  book_id uuid primary key references public.books(id) on delete cascade,
  schema_version integer not null default 1,
  payload jsonb not null default '{"cities":{},"memories":{},"settings":{}}'::jsonb,
  revision bigint not null default 0 check (revision >= 0),
  updated_at timestamptz not null default now(),
  constraint book_data_payload_object check (jsonb_typeof(payload) = 'object')
);

create index if not exists idx_book_members_user on public.book_members(user_id);
create index if not exists idx_book_members_book_status on public.book_members(book_id,status);
create index if not exists idx_books_created_by on public.books(created_by);

-- RLS
alter table public.books enable row level security;
alter table public.book_members enable row level security;
alter table public.book_data enable row level security;

-- 清理旧/重复 policy，保证脚本可以安全重跑。
drop policy if exists "books_select_members" on public.books;
drop policy if exists "books_update_owner" on public.books;
drop policy if exists "book_members_select" on public.book_members;
drop policy if exists "book_data_select_members" on public.book_data;
drop policy if exists "book_data_insert_editors" on public.book_data;
drop policy if exists "book_data_update_editors" on public.book_data;
drop policy if exists "book_data_delete_owner" on public.book_data;

-- book_members 在周年版只允许用户读取“自己的成员关系”。
-- 这样其他表在 RLS 中查询 book_members 时不会形成递归。
create policy "book_members_select"
on public.book_members
for select
to authenticated
using (
  user_id = auth.uid()
);

-- 用户可查看自己创建的 Book，或自己是 active member 的 Book。
create policy "books_select_members"
on public.books
for select
to authenticated
using (
  created_by = auth.uid()
  or exists (
    select 1
    from public.book_members bm
    where bm.book_id = books.id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
  )
);

-- 只有 owner 可修改 Book 元信息。
create policy "books_update_owner"
on public.books
for update
to authenticated
using (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = books.id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role = 'owner'
  )
)
with check (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = books.id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role = 'owner'
  )
);

-- book_data：active member 可读。
create policy "book_data_select_members"
on public.book_data
for select
to authenticated
using (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = book_data.book_id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
  )
);

-- owner/editor 可创建和更新周年桥接数据。
create policy "book_data_insert_editors"
on public.book_data
for insert
to authenticated
with check (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = book_data.book_id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
);

create policy "book_data_update_editors"
on public.book_data
for update
to authenticated
using (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = book_data.book_id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
)
with check (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = book_data.book_id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
);

create policy "book_data_delete_owner"
on public.book_data
for delete
to authenticated
using (
  exists (
    select 1
    from public.book_members bm
    where bm.book_id = book_data.book_id
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role = 'owner'
  )
);

-- Data API 最小授权；真正行级权限仍由 RLS 控制。
revoke all on table public.books from anon;
revoke all on table public.book_members from anon;
revoke all on table public.book_data from anon;

grant usage on schema public to authenticated;
grant select, update on table public.books to authenticated;
grant select on table public.book_members to authenticated;
grant select, insert, update, delete on table public.book_data to authenticated;

-- Private Storage Bucket：25 MiB 单文件上限。
insert into storage.buckets (id,name,public,file_size_limit)
values ('starbook-media','starbook-media',false,26214400)
on conflict (id) do update
set public = false,
    file_size_limit = excluded.file_size_limit;

-- Storage policies。对象路径第一段必须是 book_id：
-- {book_id}/images/...
-- {book_id}/audio/...
drop policy if exists "starbook_media_select_members" on storage.objects;
drop policy if exists "starbook_media_insert_editors" on storage.objects;
drop policy if exists "starbook_media_update_editors" on storage.objects;
drop policy if exists "starbook_media_delete_editors" on storage.objects;

create policy "starbook_media_select_members"
on storage.objects
for select
to authenticated
using (
  bucket_id = 'starbook-media'
  and exists (
    select 1
    from public.book_members bm
    where bm.book_id::text = coalesce((storage.foldername(name))[1],'')
      and bm.user_id = auth.uid()
      and bm.status = 'active'
  )
);

create policy "starbook_media_insert_editors"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'starbook-media'
  and exists (
    select 1
    from public.book_members bm
    where bm.book_id::text = coalesce((storage.foldername(name))[1],'')
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
);

create policy "starbook_media_update_editors"
on storage.objects
for update
to authenticated
using (
  bucket_id = 'starbook-media'
  and exists (
    select 1
    from public.book_members bm
    where bm.book_id::text = coalesce((storage.foldername(name))[1],'')
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
)
with check (
  bucket_id = 'starbook-media'
  and exists (
    select 1
    from public.book_members bm
    where bm.book_id::text = coalesce((storage.foldername(name))[1],'')
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
);

create policy "starbook_media_delete_editors"
on storage.objects
for delete
to authenticated
using (
  bucket_id = 'starbook-media'
  and exists (
    select 1
    from public.book_members bm
    where bm.book_id::text = coalesce((storage.foldername(name))[1],'')
      and bm.user_id = auth.uid()
      and bm.status = 'active'
      and bm.role in ('owner','editor')
  )
);

commit;
