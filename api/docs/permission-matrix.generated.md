# API 权限矩阵（自动生成草稿）

- 统计范围：`api/api/*/views.py`
- 权限推断规则：`get_current_super_user` > `get_current_user` > `refresh_security` > `Public`

## `api/friend`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/friend/list` | `Public` |
| GET | `/api/friend/read/{item_id}` | `Public` |
| POST | `/api/friend/create` | `Auth` |
| POST | `/api/friend/create/all` | `Auth` |
| PUT | `/api/friend/{item_id}` | `Auth` |
| PUT | `/api/friend/update/all` | `Auth` |
| DELETE | `/api/friend/{item_ids}` | `Auth` |
| DELETE | `/api/friend/delete/all` | `Auth` |
| POST | `/api/friend/siteinfo` | `Auth` |

## `api/links`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/links/list` | `Public` |
| GET | `/api/links/read/{item_id}` | `Public` |
| POST | `/api/links/create` | `Auth` |
| POST | `/api/links/create/all` | `Auth` |
| PUT | `/api/links/{item_id}` | `Auth` |
| PUT | `/api/links/update/all` | `Auth` |
| DELETE | `/api/links/{item_ids}` | `Auth` |
| DELETE | `/api/links/delete/all` | `Auth` |
| POST | `/api/links/sync_cdn` | `Auth` |
| POST | `/api/links/sync_cdn_file` | `Auth` |
| POST | `/api/links/siteinfo` | `Auth` |
| POST | `/api/links/sync_cdn_batch` | `Auth` |
| GET | `/api/links/export` | `Auth` |
| POST | `/api/links/import` | `Auth` |

## `api/menu`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/menu/list` | `Public` |
| GET | `/api/menu/read/{item_id}` | `Public` |
| POST | `/api/menu/create` | `Auth` |
| POST | `/api/menu/create/all` | `Auth` |
| PUT | `/api/menu/{item_id}` | `Auth` |
| PUT | `/api/menu/update/all` | `Auth` |
| DELETE | `/api/menu/{item_ids}` | `Auth` |
| DELETE | `/api/menu/delete/all` | `Auth` |
| GET | `/api/menu/tree` | `Public` |
| GET | `/api/menu/export` | `Auth` |
| POST | `/api/menu/import` | `Auth` |

## `api/site`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/site/update` | `Auth` |
| GET | `/api/site/get` | `Public` |
| POST | `/api/site/upload/` | `Auth` |
| GET | `/api/site/get_image/{filename}` | `Public` |
| POST | `/api/site/clear_cache` | `Auth` |
| POST | `/api/site/backup` | `Auth` |
| GET | `/api/site/backup/list` | `Auth` |
| GET | `/api/site/backup/download/{filename}` | `Auth` |
| DELETE | `/api/site/backup/{filename}` | `Auth` |
| POST | `/api/site/restore` | `Auth` |

## `api/spider`

| 方法 | 路径 | 权限 |
|---|---|---|
| GET | `/api/spider/yiyan` | `Public` |
| GET | `/api/spider/hot` | `Public` |
| GET | `/api/spider/weather` | `Public` |
