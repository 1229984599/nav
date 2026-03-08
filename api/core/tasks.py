import uuid
from typing import Any

from fastapi import WebSocket
from loguru import logger

# In-memory task store: task_id -> task info
_tasks: dict[str, dict[str, Any]] = {}


def create_task_id() -> str:
    return uuid.uuid4().hex


def register_task(task_id: str) -> None:
    _tasks[task_id] = {
        "status": "pending",
        "result": None,
        "websocket": None,
    }


def get_task(task_id: str) -> dict[str, Any] | None:
    return _tasks.get(task_id)


def set_task_websocket(task_id: str, ws: WebSocket) -> None:
    task = _tasks.get(task_id)
    if task:
        task["websocket"] = ws


def remove_task_websocket(task_id: str) -> None:
    task = _tasks.get(task_id)
    if task:
        task["websocket"] = None


async def complete_task(task_id: str, result: dict) -> None:
    task = _tasks.get(task_id)
    if not task:
        return
    task["status"] = "completed"
    task["result"] = result
    ws: WebSocket | None = task.get("websocket")
    if ws:
        try:
            await ws.send_json({"type": "task_completed", "task_id": task_id, "data": result})
        except Exception as e:
            logger.warning(f"Failed to send WS message for task {task_id}: {e}")


async def fail_task(task_id: str, error: str) -> None:
    task = _tasks.get(task_id)
    if not task:
        return
    task["status"] = "failed"
    task["result"] = {"error": error}
    ws: WebSocket | None = task.get("websocket")
    if ws:
        try:
            await ws.send_json({"type": "task_failed", "task_id": task_id, "data": {"error": error}})
        except Exception as e:
            logger.warning(f"Failed to send WS error for task {task_id}: {e}")


def cleanup_task(task_id: str) -> None:
    _tasks.pop(task_id, None)
