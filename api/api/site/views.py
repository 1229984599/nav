import asyncio
import json
import shutil
from datetime import datetime
from pathlib import Path

from fastapi_cache import FastAPICache

from fastapi_cache.decorator import cache

from starlette.responses import FileResponse
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
from common.response import BaseApiOut

from models import Site, Menu, Links, Friend, User, CorsOrigin
from .schemas import SiteSchemaList, SiteSchemaPublic, SiteSchemaUpdate
from auth.auth import get_current_user, get_current_super_user
from settings import settings
from core.tasks import create_task_id, register_task, complete_task, fail_task, send_task_progress, track_task

site_router = APIRouter()


@site_router.post('/update', response_model=BaseApiOut[SiteSchemaUpdate], dependencies=[Depends(get_current_user)])
async def handle_update_site(site: SiteSchemaUpdate):
    """
    创更新数据
    """
    first_model = await Site.first()
    if not first_model:
        raise HTTPException(status_code=404, detail="站点信息未初始化")
    await first_model.update_from_dict(site.model_dump(exclude_unset=True, exclude={"id"}))
    await first_model.save()
    # data = await Site.update_one(site.id, site.dict(exclude_unset=True, exclude={"id"}))
    # site_info = await Site.get_or_none(id=data)
    data = SiteSchemaUpdate.model_validate(first_model, from_attributes=True)
    # 清除链接缓存
    await FastAPICache.clear(namespace='site')
    return BaseApiOut(data=data)


@site_router.get('/get', response_model=BaseApiOut)
@cache(expire=60 * 60 * 24, namespace='site')
async def handle_get_site():
    """
    获取数据站点（公开接口，不返回敏感字段）
    """
    data = await Site.first()
    if not data:
        return BaseApiOut(data=None)
    payload = SiteSchemaPublic.model_validate(data, from_attributes=True)
    return BaseApiOut(data=payload)


@site_router.get('/stats', response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def handle_stats():
    """获取系统统计数据（供 Dashboard 使用）"""
    link_count = await Links.all().count()
    menu_count = await Menu.all().count()
    friend_count = await Friend.all().count()
    user_count = await User.all().count()
    # 每个分类下的链接数分布
    menus = await Menu.filter(parent_id=None).prefetch_related("links")
    distribution = []
    for m in menus:
        count = len(m.links)
        if count > 0:
            distribution.append({"name": m.title, "value": count})
    # 最近添加的链接
    recent = await Links.all().order_by("-create_time").limit(8).values(
        "id", "title", "href", "icon", "create_time"
    )
    recent_links = [
        {
            "id": r["id"],
            "title": r["title"],
            "href": r["href"],
            "icon": r["icon"],
            "create_time": r["create_time"].strftime("%Y-%m-%d %H:%M") if r["create_time"] else "",
        }
        for r in recent
    ]
    return BaseApiOut(data={
        "link_count": link_count,
        "menu_count": menu_count,
        "friend_count": friend_count,
        "user_count": user_count,
        "distribution": distribution,
        "recent_links": recent_links,
    })


# 上传图片的路由和处理函数
@site_router.post("/upload/", response_model=BaseApiOut, dependencies=[Depends(get_current_user)])
async def upload_image(request: Request, file: UploadFile = File(...)):
    img_path = settings.BASE_PATH.joinpath('img').joinpath('logo.png')
    with open(img_path, "wb") as f:
        f.write(file.file.read())
    img_url = f"{request.base_url}api/site/get_image/logo.png"
    return BaseApiOut(data={"img_url": img_url})


# 访问图片的路由和处理函数
@site_router.get("/get_image/{filename}")
async def get_image(filename: str):
    # 防止路径遍历攻击
    safe_name = Path(filename).name
    if safe_name != filename or '..' in filename:
        raise HTTPException(status_code=400, detail="非法文件名")
    img_path = settings.BASE_PATH.joinpath('img').joinpath(safe_name)
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(img_path)


@site_router.post('/clear_cache', dependencies=[Depends(get_current_user)])
async def handle_clear_cache():
    """
    清除缓存
    """
    await FastAPICache.clear()
    from api.menu.views import invalidate_tree_cache
    invalidate_tree_cache()
    return BaseApiOut(message='缓存清除成功')


BACKUP_DIR = settings.BASE_PATH / "data" / "backups"


@site_router.post('/backup', dependencies=[Depends(get_current_super_user)])
async def handle_backup():
    """全站数据备份为JSON文件（后台任务 + WebSocket进度推送）"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    task_id = create_task_id()
    register_task(task_id)

    async def _run_backup():
        try:
            total_steps = 7

            # Step 1: Site settings
            await send_task_progress(task_id, {
                "step": "site", "current": 1, "total": total_steps,
                "message": "正在收集站点设置..."
            })
            site = await Site.first()
            site_data = None
            if site:
                site_data = {
                    "title": site.title, "desc": site.desc, "keywords": site.keywords,
                    "icon": site.icon, "color": site.color, "footer": site.footer,
                    "yiyan": site.yiyan, "weather": site.weather, "weather_key": site.weather_key,
                    "copyright": site.copyright, "cdn_img_token": site.cdn_img_token,
                }

            # Step 2: CORS origins
            await send_task_progress(task_id, {
                "step": "cors", "current": 2, "total": total_steps,
                "message": "正在收集跨域配置..."
            })
            cors_list = await CorsOrigin.all().order_by("order")
            cors_data = []
            for c in cors_list:
                cors_data.append({
                    "origin": c.origin, "desc": c.desc,
                    "order": c.order, "status": c.status,
                })

            # Step 3: Menus
            await send_task_progress(task_id, {
                "step": "menus", "current": 3, "total": total_steps,
                "message": "正在收集菜单数据..."
            })
            menus = await Menu.all().order_by("order").select_related("parent")
            menus_data = []
            for m in menus:
                menus_data.append({
                    "id": m.id,
                    "title": m.title, "icon": m.icon, "color": m.color,
                    "order": m.order, "is_vip": m.is_vip, "status": m.status,
                    "parent_id": m.parent_id,
                    "parent_title": m.parent.title if m.parent else None,
                })

            # Step 4: Links
            await send_task_progress(task_id, {
                "step": "links", "current": 4, "total": total_steps,
                "message": "正在收集链接数据..."
            })
            links = await Links.all().order_by("order").prefetch_related("menus")
            links_data = []
            for link in links:
                link_menus = link.menus  # 已 prefetch_related，直接访问无需 await
                links_data.append({
                    "title": link.title, "href": link.href, "icon": link.icon,
                    "desc": link.desc, "color": link.color, "is_self": link.is_self,
                    "is_vip": link.is_vip, "order": link.order, "cdn_img_id": link.cdn_img_id,
                    "status": link.status, "menus": [m.title for m in link_menus],
                })

            # Step 5: Friends
            await send_task_progress(task_id, {
                "step": "friends", "current": 5, "total": total_steps,
                "message": "正在收集友链数据..."
            })
            friends = await Friend.all().order_by("order")
            friends_data = []
            for f in friends:
                friends_data.append({
                    "title": f.title, "href": f.href, "icon": f.icon,
                    "desc": f.desc, "color": f.color, "order": f.order, "status": f.status,
                })

            # Step 6: Users
            await send_task_progress(task_id, {
                "step": "users", "current": 6, "total": total_steps,
                "message": "正在收集用户数据..."
            })
            users = await User.all().order_by("order")
            users_data = []
            for u in users:
                users_data.append({
                    "username": u.username, "password": u.password, "nickname": u.nickname,
                    "status": u.status, "is_super": u.is_super, "order": u.order,
                })

            # Step 7: Write file
            await send_task_progress(task_id, {
                "step": "write", "current": 7, "total": total_steps,
                "message": "正在写入备份文件..."
            })
            backup = {
                "version": 2,
                "created_at": datetime.now().isoformat(),
                "site": site_data,
                "cors_origins": cors_data,
                "menus": menus_data,
                "links": links_data,
                "friends": friends_data,
                "users": users_data,
            }
            filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = BACKUP_DIR / filename
            filepath.write_text(json.dumps(backup, ensure_ascii=False, indent=2), encoding="utf-8")

            await complete_task(task_id, {"filename": filename, "path": str(filepath)})
        except Exception as e:
            await fail_task(task_id, str(e))

    track_task(_run_backup())
    return BaseApiOut(data={"task_id": task_id})


@site_router.get('/backup/list', dependencies=[Depends(get_current_super_user)])
async def handle_backup_list():
    """列出所有备份文件"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(BACKUP_DIR.glob("backup_*.json"), reverse=True)
    result = []
    for f in files:
        stat = f.stat()
        result.append({
            "filename": f.name,
            "size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })
    return BaseApiOut(data=result)


@site_router.get('/backup/download/{filename}', dependencies=[Depends(get_current_super_user)])
async def handle_backup_download(filename: str):
    """下载指定备份文件"""
    safe_name = Path(filename).name
    if safe_name != filename or '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="非法文件名")
    filepath = BACKUP_DIR / safe_name
    if not filepath.exists() or not safe_name.startswith("backup_"):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    return FileResponse(filepath, filename=safe_name, media_type="application/json")


@site_router.delete('/backup/{filename}', dependencies=[Depends(get_current_super_user)])
async def handle_backup_delete(filename: str):
    """删除指定备份文件"""
    safe_name = Path(filename).name
    if safe_name != filename or '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="非法文件名")
    filepath = BACKUP_DIR / safe_name
    if not filepath.exists() or not safe_name.startswith("backup_"):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    filepath.unlink()
    return BaseApiOut(message="备份文件已删除")


@site_router.post('/restore', dependencies=[Depends(get_current_super_user)])
async def handle_restore(filename: str = "", file: UploadFile | None = File(None)):
    """从备份文件恢复全站数据（后台任务 + WebSocket进度推送）"""
    if file and file.filename:
        content = await file.read()
    elif filename:
        filepath = BACKUP_DIR / filename
        if not filepath.exists():
            raise HTTPException(status_code=404, detail="备份文件不存在")
        content = filepath.read_bytes()
    else:
        raise HTTPException(status_code=400, detail="请上传备份文件或指定备份文件名")

    try:
        backup = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON格式错误")

    task_id = create_task_id()
    register_task(task_id)

    async def _run_restore():
        try:
            from tortoise.transactions import in_transaction

            steps = []
            if backup.get("site"): steps.append("site")
            if backup.get("cors_origins"): steps.append("cors")
            if backup.get("menus"): steps.append("menus")
            if backup.get("links"): steps.append("links")
            if backup.get("friends"): steps.append("friends")
            if backup.get("users"): steps.append("users")
            total_steps = len(steps)
            current_step = 0

            async with in_transaction():
                # Restore site settings
                if backup.get("site"):
                    current_step += 1
                    await send_task_progress(task_id, {
                        "step": "site", "current": current_step, "total": total_steps,
                        "message": "正在恢复站点设置..."
                    })
                    site = await Site.first()
                    site_dict = {k: v for k, v in backup["site"].items() if k != "cors_origins"}
                    if site:
                        await site.update_from_dict(site_dict)
                        await site.save()

                # Restore CORS origins
                if backup.get("cors_origins"):
                    current_step += 1
                    await send_task_progress(task_id, {
                        "step": "cors", "current": current_step, "total": total_steps,
                        "message": f"正在恢复跨域配置（共 {len(backup['cors_origins'])} 条）..."
                    })
                    await CorsOrigin.all().delete()
                    cors_items = backup["cors_origins"]
                    if cors_items and isinstance(cors_items[0], str):
                        # 兼容旧版 v1 格式：cors_origins 是字符串数组
                        for i, origin in enumerate(cors_items):
                            await CorsOrigin.create(origin=origin, order=i, status=True)
                    else:
                        for item in cors_items:
                            await CorsOrigin.create(**item)

                # Restore menus
                if backup.get("menus"):
                    current_step += 1
                    await send_task_progress(task_id, {
                        "step": "menus", "current": current_step, "total": total_steps,
                        "message": f"正在恢复菜单数据（共 {len(backup['menus'])} 条）..."
                    })
                    await Menu.all().delete()
                    id_map: dict[int, int] = {}
                    title_map: dict[str, int] = {}
                    pending_parent: list[tuple[int, int | None, str | None]] = []

                    for raw in backup["menus"]:
                        item = dict(raw or {})
                        old_id = item.get("id")
                        old_parent_id = item.get("parent_id")
                        parent_title = item.get("parent_title")

                        payload = {
                            "title": item.get("title"),
                            "icon": item.get("icon"),
                            "color": item.get("color"),
                            "order": item.get("order", 0),
                            "is_vip": item.get("is_vip", False),
                            "status": item.get("status", True),
                        }
                        menu = await Menu.create(**payload)

                        if isinstance(old_id, int):
                            id_map[old_id] = menu.id
                        if menu.title:
                            title_map[menu.title] = menu.id
                        pending_parent.append((menu.id, old_parent_id, parent_title))

                    for menu_id, old_parent_id, parent_title in pending_parent:
                        new_parent_id = None
                        if isinstance(old_parent_id, int):
                            new_parent_id = id_map.get(old_parent_id)
                        if not new_parent_id and parent_title:
                            new_parent_id = title_map.get(parent_title)
                        if new_parent_id and new_parent_id != menu_id:
                            await Menu.filter(id=menu_id).update(parent_id=new_parent_id)

                # Restore links
                if backup.get("links"):
                    current_step += 1
                    total_links = len(backup["links"])
                    await send_task_progress(task_id, {
                        "step": "links", "current": current_step, "total": total_steps,
                        "message": f"正在恢复链接数据（共 {total_links} 条）..."
                    })
                    await Links.all().delete()
                    menu_map = {m.title: m for m in await Menu.all()}
                    for i, item in enumerate(backup["links"]):
                        menu_titles = item.pop("menus", []) or []
                        link = await Links.create(**item)
                        menus_to_add = [menu_map[t] for t in menu_titles if t in menu_map]
                        if menus_to_add:
                            await link.menus.add(*menus_to_add)
                        if (i + 1) % 20 == 0 or (i + 1) == total_links:
                            await send_task_progress(task_id, {
                                "step": "links", "current": current_step, "total": total_steps,
                                "message": f"正在恢复链接数据（{i + 1}/{total_links}）...",
                                "detail_current": i + 1,
                                "detail_total": total_links,
                            })

                # Restore friends
                if backup.get("friends"):
                    current_step += 1
                    await send_task_progress(task_id, {
                        "step": "friends", "current": current_step, "total": total_steps,
                        "message": f"正在恢复友链数据（共 {len(backup['friends'])} 条）..."
                    })
                    await Friend.all().delete()
                    for item in backup["friends"]:
                        await Friend.create(**item)

                # Restore users
                if backup.get("users"):
                    current_step += 1
                    await send_task_progress(task_id, {
                        "step": "users", "current": current_step, "total": total_steps,
                        "message": f"正在恢复用户数据（共 {len(backup['users'])} 条）..."
                    })
                    await User.all().delete()
                    for item in backup["users"]:
                        await User.create(**item)

            await FastAPICache.clear()
            from api.menu.views import invalidate_tree_cache
            invalidate_tree_cache()
            # 恢复后刷新 CORS 缓存
            from core.middleware import load_cors_origins
            await load_cors_origins()

            await complete_task(task_id, {"message": "数据恢复成功"})
        except Exception as e:
            await fail_task(task_id, str(e))

    track_task(_run_restore())
    return BaseApiOut(data={"task_id": task_id})
