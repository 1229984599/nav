from __future__ import annotations

import json
from dataclasses import dataclass

import bcrypt
from loguru import logger
from tortoise import Tortoise

from models import Site, User
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


async def apply_runtime_migrations() -> None:
    dialect = _get_db_dialect()
    connection = Tortoise.get_connection("default")

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
        created=created,
        skipped=skipped,
        dialect=dialect,
        total=len(INDEX_SPECS),
    )


async def seed_initial_data() -> None:
    if not await User.all().exists():
        _log_event("seed_user_create", username="admin")
        await User.create(
            username="admin",
            password=_get_password_hash("admina"),
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


@ignore_async_errors
async def init_data() -> None:
    _log_event("runtime_migration_start")
    await Tortoise.init(config=settings.DATABASE_CONFIG)
    await Tortoise.generate_schemas()
    await apply_runtime_migrations()
    await seed_initial_data()
    await Tortoise.close_connections()
    _log_event("runtime_migration_finish")
