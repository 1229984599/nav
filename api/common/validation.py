import ipaddress
import socket
from typing import Any
from urllib.parse import urlparse

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


def validate_external_url(url: str) -> None:
    """校验 URL 不指向内网地址，防止 SSRF 攻击。"""
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="URL 格式无效")

    # 禁止直接使用内网主机名
    if hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        raise HTTPException(status_code=400, detail="不允许访问内网地址")

    try:
        resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="无法解析主机名")

    for family, _, _, _, sockaddr in resolved:
        ip = ipaddress.ip_address(sockaddr[0])
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
            raise HTTPException(status_code=400, detail="不允许访问内网地址")

