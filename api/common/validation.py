from typing import Any

from fastapi import HTTPException


def parse_order_by(order_by: str, allowed_fields: set[str], *, default: str = "-create_time", resource: str = "资源") -> list[str]:
    if not order_by:
        return [default]

    fields: list[str] = []
    invalid_fields: list[str] = []
    for raw in order_by.split(","):
        field = raw.strip()
        if not field:
            continue
        clean = field[1:] if field.startswith("-") else field
        if clean not in allowed_fields:
            invalid_fields.append(clean)
            continue
        fields.append(field)

    if not fields:
        raise HTTPException(status_code=422, detail=f"{resource}排序字段非法: {', '.join(invalid_fields) or order_by}")
    return fields


def validate_batch_size(items: list[Any], *, max_size: int, batch_name: str) -> None:
    if len(items) > max_size:
        raise HTTPException(status_code=422, detail=f"{batch_name}超过最大限制: {max_size}")

