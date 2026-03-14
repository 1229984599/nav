import uuid
import time
import asyncio
from typing import Any

from fastapi import WebSocket
from loguru import logger

# In-memory task store: task_id -> task info
_tasks: dict[str, dict[str, Any]] = {}

# Keep completed/failed tasks for 5 minutes so refreshed pages can retrieve results
_TASK_RETAIN_SECONDS = 300

# 保持后台任务引用，防止 GC 回收
_background_tasks: set[asyncio.Task] = set()


def track_task(coro) -> asyncio.Task:
    """创建后台任务并保持引用，防止被垃圾回收"""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return task


def create_task_id() -> str:
    return uuid.uuid4().hex


def register_task(task_id: str) -> None:
    _cleanup_expired()
    _tasks[task_id] = {
        "status": "pending",
        "result": None,
        "websocket": None,
        "created_at": time.time(),
        "finished_at": None,
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
    task["finished_at"] = time.time()
    ws: WebSocket | None = task.get("websocket")
    if ws:
        try:
            await ws.send_json({"type": "task_completed", "task_id": task_id, "data": result})
        except Exception as e:
            logger.warning(f"Failed to send WS message for task {task_id}: {e}")


async def send_task_progress(task_id: str, data: dict) -> None:
    """Send a progress update to the WebSocket client without changing task status."""
    task = _tasks.get(task_id)
    if not task:
        return
    ws: WebSocket | None = task.get("websocket")
    if ws:
        try:
            await ws.send_json({"type": "task_progress", "task_id": task_id, "data": data})
        except Exception:
            pass


async def fail_task(task_id: str, error: str) -> None:
    task = _tasks.get(task_id)
    if not task:
        return
    task["status"] = "failed"
    task["result"] = {"error": error}
    task["finished_at"] = time.time()
    ws: WebSocket | None = task.get("websocket")
    if ws:
        try:
            await ws.send_json({"type": "task_failed", "task_id": task_id, "data": {"error": error}})
        except Exception as e:
            logger.warning(f"Failed to send WS error for task {task_id}: {e}")


def cleanup_task(task_id: str) -> None:
    _tasks.pop(task_id, None)


def _cleanup_expired() -> None:
    """Remove finished tasks older than _TASK_RETAIN_SECONDS."""
    now = time.time()
    expired = [
        tid for tid, t in _tasks.items()
        if t.get("finished_at") and (now - t["finished_at"]) > _TASK_RETAIN_SECONDS
    ]
    for tid in expired:
        _tasks.pop(tid, None)
