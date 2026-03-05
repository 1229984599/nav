# API 权限矩阵

本文档用于约束和审计后端接口权限，避免出现“可匿名写入/删除”或“普通用户可管理系统用户”等高危问题。

## 权限级别定义

- `Public`：匿名可访问。
- `Auth`：需登录，依赖 `get_current_user`。
- `Super`：需超级管理员，依赖 `get_current_super_user`。

鉴权函数位置：`auth/auth.py`

## 当前接口矩阵

> 统计范围：`api/api/*/views.py`

### `api/friend`

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

### `api/links`

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

### `api/menu`

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

### `api/site`

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

### `api/spider`

| 方法 | 路径 | 权限 |
|---|---|---|
| GET | `/api/spider/yiyan` | `Public` |
| GET | `/api/spider/hot` | `Public` |
| GET | `/api/spider/weather` | `Public` |

### `api/system/login`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/system/login/login` | `Public` |
| POST | `/api/system/login/register` | `Super` |
| POST | `/api/system/login/refresh` | `RefreshToken` |
| POST | `/api/system/login/refreshToken` | `RefreshToken` |
| GET | `/api/system/login/me` | `Auth` |
| GET | `/api/system/login/getUserInfo` | `Auth` |
| PUT | `/api/system/login/updateProfile` | `Auth` |
| PUT | `/api/system/login/changePassword` | `Auth` |
| GET | `/api/system/login/getUserRoutes` | `Auth` |

### `api/system/user`

| 方法 | 路径 | 权限 |
|---|---|---|
| POST | `/api/system/user/list` | `Super` |
| GET | `/api/system/user/read/{item_id}` | `Super` |
| POST | `/api/system/user/create` | `Super` |
| POST | `/api/system/user/create/all` | `Super` |
| PUT | `/api/system/user/{item_id}` | `Super` |
| PUT | `/api/system/user/update/all` | `Super` |
| DELETE | `/api/system/user/{item_ids}` | `Super` |
| DELETE | `/api/system/user/delete/all` | `Super` |

## 新增接口模板（必须填写）

新增接口时，请在 PR 描述中附上如下信息，并同步更新本文件。

```text
模块：api/<module>
方法+路径：<METHOD> /api/<module>/<path>
权限级别：Public | Auth | Super
鉴权依赖：无 | Depends(get_current_user) | Depends(get_current_super_user)
风险说明：读数据 / 写数据 / 删除数据 / 文件操作 / 外部请求
```

## 安全检查清单

- 写操作（`POST/PUT/PATCH/DELETE`）默认不允许 `Public`，除非有明确业务理由。
- 用户管理、权限管理、系统配置类接口默认 `Super`。
- 涉及文件上传、备份恢复、外部请求转发的接口至少 `Auth`。
- 前端是否隐藏按钮不算鉴权，后端依赖必须强制校验。
- 新增接口后需执行一次最小验证（至少语法检查或单测）。

## 自动生成草稿

可使用脚本自动扫描 `api/api/*/views.py` 并生成权限矩阵草稿。

```bash
python scripts/generate_permission_matrix.py
```

将结果写入文件：

```bash
python scripts/generate_permission_matrix.py --output docs/permission-matrix.generated.md
```

说明：自动稿按依赖静态推断权限（`Super`/`Auth`/`RefreshToken`/`Public`），建议与本文件人工审阅后再合并。
