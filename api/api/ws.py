import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from loguru import logger

from authlib.jose import JsonWebToken
from core.tasks import get_task, set_task_websocket, remove_task_websocket
from models import User
from settings import settings

ws_router = APIRouter()

_jwt = JsonWebToken(algorithms=["HS256"])

# WebSocket 最大空闲时间（秒），超时无消息则断开
_WS_IDLE_TIMEOUT = 300


async def _authenticate_ws(token: str) -> User | None:
    """Validate JWT token from query param and return user, or None."""
    try:
        payload = _jwt.decode(token, settings.SECRET_KEY)
        payload.validate()
        username = payload.get("subject", {}).get("username")
        if not username:
            return None
        return await User.filter(username=username, status=True).first()
    except Exception:
        return None


@ws_router.websocket("/tasks/{task_id}")
async def ws_task_status(websocket: WebSocket, task_id: str, token: str = Query(...)):
    user = await _authenticate_ws(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    task = get_task(task_id)
    if not task:
        await websocket.close(code=4004, reason="Task not found")
        return

    await websocket.accept()
    set_task_websocket(task_id, websocket)

    try:
        # If task already completed before WS connected, send result immediately
        if task["status"] in ("completed", "failed"):
            msg_type = "task_completed" if task["status"] == "completed" else "task_failed"
            await websocket.send_json({"type": msg_type, "task_id": task_id, "data": task["result"]})
            await websocket.close()
            return

        # Keep connection alive; background task sends result via complete_task/fail_task
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=_WS_IDLE_TIMEOUT)
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                logger.info(f"WS idle timeout for task {task_id}")
                await websocket.close(code=4008, reason="Idle timeout")
                break
    except WebSocketDisconnect:
        logger.info(f"WS disconnected for task {task_id}")
    finally:
        remove_task_websocket(task_id)
