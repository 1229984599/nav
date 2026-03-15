from __future__ import annotations

import json
from dataclasses import dataclass

import bcrypt
from loguru import logger
from tortoise import Tortoise

from models import Site, User, CorsOrigin
from settings import settings
from utils.error import ignore_async_errors


@dataclass(frozen=True)
class IndexSpec:
    table: str
    column: str
    name: str


@dataclass(frozen=True)
class ColumnAlterSpec:
    table: str
    column: str
    new_type: str  # e.g. "VARCHAR(500)"


COLUMN_ALTER_SPECS: tuple[ColumnAlterSpec, ...] = (
    ColumnAlterSpec(table="links", column="icon", new_type="VARCHAR(500)"),
    ColumnAlterSpec(table="links", column="href", new_type="VARCHAR(500)"),
)


INDEX_SPECS: tuple[IndexSpec, ...] = (
    IndexSpec(table="menu", column="order", name="idx_menu_order_manual"),
    IndexSpec(table="menu", column="is_vip", name="idx_menu_is_vip_manual"),
    IndexSpec(table="menu", column="parent_id", name="idx_menu_parent_id_manual"),
    IndexSpec(table="links", column="order", name="idx_links_order_manual"),
    IndexSpec(table="links", column="is_vip", name="idx_links_is_vip_manual"),
    IndexSpec(table="friend", column="order", name="idx_friend_order_manual"),
)


def _log_event(event: str, **fields) -> None:
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, ensure_ascii=False, default=str))


def _get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def _get_db_dialect() -> str:
    database_uri = settings.DATABASE_URI.lower()
    if database_uri.startswith("sqlite"):
        return "sqlite"
    if database_uri.startswith("mysql"):
        return "mysql"
    if database_uri.startswith("postgres"):
        return "postgres"
    return "unknown"


async def _sqlite_has_index(connection, spec: IndexSpec) -> bool:
    _, index_rows = await connection.execute_query(f"PRAGMA index_list('{spec.table}')")
    for index_row in index_rows:
        index_name = index_row[1]
        _, column_rows = await connection.execute_query(f"PRAGMA index_info('{index_name}')")
        for column_row in column_rows:
            if column_row[2] == spec.column:
                return True
    return False


async def _mysql_has_index(connection, spec: IndexSpec) -> bool:
    _, rows = await connection.execute_query(
        f"SHOW INDEX FROM `{spec.table}` WHERE Column_name = '{spec.column}'"
    )
    return bool(rows)


async def _postgres_has_index(connection, spec: IndexSpec) -> bool:
    _, rows = await connection.execute_query(
        "SELECT 1 "
        "FROM pg_indexes "
        "WHERE schemaname = current_schema() "
        f"AND tablename = '{spec.table}' "
        f"AND indexdef ILIKE '%({spec.column})%' "
        "LIMIT 1"
    )
    return bool(rows)


async def _has_index(connection, dialect: str, spec: IndexSpec) -> bool:
    if dialect == "sqlite":
        return await _sqlite_has_index(connection, spec)
    if dialect == "mysql":
        return await _mysql_has_index(connection, spec)
    if dialect == "postgres":
        return await _postgres_has_index(connection, spec)
    return False


async def _create_index(connection, dialect: str, spec: IndexSpec) -> None:
    if dialect == "mysql":
        sql = f"CREATE INDEX {spec.name} ON {spec.table} ({spec.column})"
    else:
        sql = f"CREATE INDEX IF NOT EXISTS {spec.name} ON {spec.table} ({spec.column})"
    await connection.execute_script(sql)


async def _alter_column(connection, dialect: str, spec: ColumnAlterSpec) -> None:
    if dialect == "sqlite":
        return
    if dialect == "mysql":
        sql = f"ALTER TABLE `{spec.table}` MODIFY COLUMN `{spec.column}` {spec.new_type}"
    elif dialect == "postgres":
        sql = f"ALTER TABLE {spec.table} ALTER COLUMN {spec.column} TYPE {spec.new_type}"
    else:
        return
    try:
        await connection.execute_script(sql)
        _log_event("column_altered", table=spec.table, column=spec.column, new_type=spec.new_type)
    except Exception as error:
        _log_event("column_alter_skipped", table=spec.table, column=spec.column, reason=str(error))


async def _get_table_columns(connection, dialect: str, table: str) -> set[str]:
    """获取数据库表的现有列名集合"""
    if dialect == "sqlite":
        _, rows = await connection.execute_query(f"PRAGMA table_info('{table}')")
        return {row[1] for row in rows}
    if dialect == "mysql":
        _, rows = await connection.execute_query(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
            f"WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = DATABASE()"
        )
        return {row[0] for row in rows}
    if dialect == "postgres":
        _, rows = await connection.execute_query(
            f"SELECT column_name FROM information_schema.columns "
            f"WHERE table_name = '{table}' AND table_schema = current_schema()"
        )
        return {row[0] for row in rows}
    return set()


def _field_default_sql(field_obj) -> str:
    """根据 Tortoise 字段对象生成 SQL DEFAULT 子句"""
    default = getattr(field_obj, 'default', None)
    is_null = getattr(field_obj, 'null', False)

    # 有显式默认值且非 callable
    if default is not None and not callable(default):
        if isinstance(default, bool):
            return f" DEFAULT {1 if default else 0}"
        if isinstance(default, (int, float)):
            return f" DEFAULT {default}"
        if isinstance(default, str):
            escaped = default.replace("'", "''")
            return f" DEFAULT '{escaped}'"

    if is_null:
        return " DEFAULT NULL"

    # NOT NULL 且无默认值 —— 按类型给安全默认值（ALTER TABLE ADD COLUMN 必须有默认值）
    sql_type = getattr(field_obj, 'SQL_TYPE', 'TEXT').upper()
    if 'INT' in sql_type or 'BOOL' in sql_type or 'SMALLINT' in sql_type:
        return " DEFAULT 0"
    return " DEFAULT ''"


async def _add_missing_columns(connection, dialect: str) -> int:
    """自动检测并添加模型中新增但数据库中缺失的列（通用自动迁移）

    遍历所有已注册的 Tortoise 模型，对比模型字段与数据库实际列，
    自动补全缺失的列。以后模型新增任何字段，启动时都会自动迁移。
    """
    added = 0

    for app_models in Tortoise.apps.values():
        for model_cls in app_models.values():
            meta = model_cls._meta
            if getattr(meta, 'abstract', False):
                continue

            table = meta.db_table
            existing_cols = await _get_table_columns(connection, dialect, table)
            if not existing_cols:
                continue  # 表不存在，generate_schemas() 会创建

            # fields_db_projection: {model_field_name: db_column_name}
            # 仅包含真正存储在表中的字段（排除 M2M、反向关联等）
            for field_name, db_col in meta.fields_db_projection.items():
                if db_col in existing_cols:
                    continue

                field_obj = meta.fields_map.get(field_name)
                if not field_obj:
                    continue

                sql_type = getattr(field_obj, 'SQL_TYPE', 'TEXT')
                default_clause = _field_default_sql(field_obj)
                null_clause = " NULL" if getattr(field_obj, 'null', False) else ""

                sql = f'ALTER TABLE "{table}" ADD COLUMN "{db_col}" {sql_type}{null_clause}{default_clause}'
                try:
                    await connection.execute_script(sql)
                    _log_event("column_added", table=table, column=db_col, type=sql_type)
                    added += 1
                except Exception as e:
                    msg = str(e).lower()
                    if "duplicate" in msg or "already exists" in msg:
                        continue
                    _log_event("column_add_failed", table=table, column=db_col, error=str(e))

    return added


async def apply_runtime_migrations() -> None:
    dialect = _get_db_dialect()
    connection = Tortoise.get_connection("default")

    # 自动补全缺失列（模型新增字段自动迁移）
    cols_added = await _add_missing_columns(connection, dialect)

    # Column alterations
    for spec in COLUMN_ALTER_SPECS:
        await _alter_column(connection, dialect, spec)

    # Index creation
    created = 0
    skipped = 0
    for spec in INDEX_SPECS:
        if await _has_index(connection, dialect, spec):
            skipped += 1
            continue
        try:
            await _create_index(connection, dialect, spec)
            created += 1
        except Exception as error:
            message = str(error).lower()
            if "duplicate" in message or "already exists" in message:
                skipped += 1
                continue
            raise

    _log_event(
        "runtime_migration_completed",
        columns_added=cols_added,
        indexes_created=created,
        indexes_skipped=skipped,
        dialect=dialect,
    )


async def seed_initial_data() -> None:
    if not await User.all().exists():
        import secrets
        default_password = secrets.token_urlsafe(12)
        _log_event("seed_user_create", username="admin", password=default_password)
        logger.warning(f"[初始化] 默认管理员账号: admin  密码: {default_password}  请及时修改！")
        await User.create(
            username="admin",
            password=_get_password_hash(default_password),
            nickname="超级管理员",
            status=True,
            is_super=True,
        )

    if not await Site.all().exists():
        _log_event("seed_site_create", title="哈哈导航")
        await Site.create(
            title="哈哈导航",
            icon="ion:logo-edge",
            desc="哈哈导航",
            keywords="哈哈导航",
            color="#104A84",
            copyright="渝ICP备2021008654号",
            footer="Copyright © 2023 哈哈导航. All Rights Reserved.",
        )

    # 迁移旧版 Site.cors_origins JSON 数据到 CorsOrigin 表
    if not await CorsOrigin.all().exists():
        connection = Tortoise.get_connection("default")
        dialect = _get_db_dialect()
        existing_cols = await _get_table_columns(connection, dialect, "site")
        if "cors_origins" in existing_cols:
            site = await Site.first()
            if site:
                try:
                    raw = getattr(site, 'cors_origins', None)
                    if raw:
                        origins = json.loads(raw) if isinstance(raw, str) else raw
                        if isinstance(origins, list):
                            for i, origin in enumerate(origins):
                                if isinstance(origin, str) and origin.strip():
                                    await CorsOrigin.create(
                                        origin=origin.strip(), order=i, status=True,
                                    )
                            if origins:
                                _log_event("cors_migrated", count=len(origins))
                except Exception as e:
                    _log_event("cors_migration_skipped", reason=str(e))


@ignore_async_errors
async def init_data() -> None:
    _log_event("runtime_migration_start")
    await Tortoise.init(config=settings.DATABASE_CONFIG)
    await Tortoise.generate_schemas()
    await apply_runtime_migrations()
    await seed_initial_data()
    await Tortoise.close_connections()
    _log_event("runtime_migration_finish")
