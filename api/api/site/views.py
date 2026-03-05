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

from models import Site, Menu, Links, Friend, User
from .schemas import SiteSchemaList, SiteSchemaUpdate
from auth.auth import get_current_user
from settings import settings

site_router = APIRouter()


@site_router.post('/update', response_model=BaseApiOut[SiteSchemaUpdate], dependencies=[Depends(get_current_user)])
async def handle_update_site(site: SiteSchemaUpdate):
    """
    创更新数据
    """
    first_model = await Site.first()
    await first_model.update_from_dict(site.model_dump(exclude_unset=True, exclude={"id"}))
    await first_model.save()
    # data = await Site.update_one(site.id, site.dict(exclude_unset=True, exclude={"id"}))
    # site_info = await Site.get_or_none(id=data)
    data = SiteSchemaUpdate.model_validate(first_model, from_attributes=True)
    # 清除链接缓存
    await FastAPICache.clear(namespace='site')
    return BaseApiOut(data=data)


@site_router.get('/get', response_model=BaseApiOut)
# 站点数据，几乎不会改变，缓存30天
# @cache(expire=60 * 60 * 24 * 30, namespace='site')
async def handle_get_site():
    """
    获取数据站点
    """
    data = await Site.first()
    payload = SiteSchemaList.model_validate(data, from_attributes=True)
    return BaseApiOut(data=payload)


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
    img_path = settings.BASE_PATH.joinpath('img').joinpath(filename)
    return FileResponse(img_path)


@site_router.post('/clear_cache', dependencies=[Depends(get_current_user)])
async def handle_clear_cache():
    """
    清除缓存
    """
    data = await FastAPICache.clear()
    return BaseApiOut(message='缓存清除成功')


BACKUP_DIR = settings.BASE_PATH / "data" / "backups"


@site_router.post('/backup', dependencies=[Depends(get_current_user)])
async def handle_backup():
    """全站数据备份为JSON文件，保存到 api/data/backups/"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # 收集站点设置
    site = await Site.first()
    site_data = None
    if site:
        site_data = {
            "title": site.title, "desc": site.desc, "keywords": site.keywords,
            "icon": site.icon, "color": site.color, "footer": site.footer,
            "yiyan": site.yiyan, "weather": site.weather, "weather_key": site.weather_key,
            "copyright": site.copyright, "cdn_img_token": site.cdn_img_token,
        }

    # 收集菜单
    menus = await Menu.all().order_by("order").select_related("parent")
    menus_data = []
    for m in menus:
        menus_data.append({
            "title": m.title, "icon": m.icon, "color": m.color,
            "order": m.order, "is_vip": m.is_vip, "status": m.status,
            "parent_title": m.parent.title if m.parent else None,
        })

    # 收集链接（含菜单关联）
    links = await Links.all().order_by("order").prefetch_related("menus")
    links_data = []
    for link in links:
        link_menus = await link.menus.all()
        links_data.append({
            "title": link.title, "href": link.href, "icon": link.icon,
            "desc": link.desc, "color": link.color, "is_self": link.is_self,
            "is_vip": link.is_vip, "order": link.order, "cdn_img_id": link.cdn_img_id,
            "status": link.status, "menus": [m.title for m in link_menus],
        })

    # 收集友链
    friends = await Friend.all().order_by("order")
    friends_data = []
    for f in friends:
        friends_data.append({
            "title": f.title, "href": f.href, "icon": f.icon,
            "desc": f.desc, "color": f.color, "order": f.order, "status": f.status,
        })

    # 收集用户
    users = await User.all().order_by("order")
    users_data = []
    for u in users:
        users_data.append({
            "username": u.username, "password": u.password, "nickname": u.nickname,
            "status": u.status, "is_super": u.is_super, "order": u.order,
        })

    backup = {
        "version": 1,
        "created_at": datetime.now().isoformat(),
        "site": site_data,
        "menus": menus_data,
        "links": links_data,
        "friends": friends_data,
        "users": users_data,
    }

    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = BACKUP_DIR / filename
    filepath.write_text(json.dumps(backup, ensure_ascii=False, indent=2), encoding="utf-8")

    return BaseApiOut(data={"filename": filename, "path": str(filepath)})


@site_router.get('/backup/list', dependencies=[Depends(get_current_user)])
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


@site_router.get('/backup/download/{filename}', dependencies=[Depends(get_current_user)])
async def handle_backup_download(filename: str):
    """下载指定备份文件"""
    filepath = BACKUP_DIR / filename
    if not filepath.exists() or not filepath.name.startswith("backup_"):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    return FileResponse(filepath, filename=filename, media_type="application/json")


@site_router.delete('/backup/{filename}', dependencies=[Depends(get_current_user)])
async def handle_backup_delete(filename: str):
    """删除指定备份文件"""
    filepath = BACKUP_DIR / filename
    if not filepath.exists() or not filepath.name.startswith("backup_"):
        raise HTTPException(status_code=404, detail="备份文件不存在")
    filepath.unlink()
    return BaseApiOut(message="备份文件已删除")


@site_router.post('/restore', dependencies=[Depends(get_current_user)])
async def handle_restore(filename: str = "", file: UploadFile | None = File(None)):
    """从备份文件恢复全站数据。支持上传文件或指定已有备份文件名"""
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

    # 恢复站点设置
    if backup.get("site"):
        site = await Site.first()
        if site:
            await site.update_from_dict(backup["site"])
            await site.save()

    # 恢复菜单
    if backup.get("menus"):
        await Menu.all().delete()
        for item in backup["menus"]:
            parent_title = item.pop("parent_title", None)
            await Menu.create(**item)
        # 第二遍设置父级
        for item in backup["menus"]:
            parent_title = item.get("parent_title")
            if not parent_title:
                continue
            menu = await Menu.filter(title=item["title"]).first()
            parent = await Menu.filter(title=parent_title).first()
            if menu and parent:
                menu.parent_id = parent.id
                await menu.save()

    # 恢复链接
    if backup.get("links"):
        await Links.all().delete()
        menu_map = {m.title: m for m in await Menu.all()}
        for item in backup["links"]:
            menu_titles = item.pop("menus", []) or []
            link = await Links.create(**item)
            menus_to_add = [menu_map[t] for t in menu_titles if t in menu_map]
            if menus_to_add:
                await link.menus.add(*menus_to_add)

    # 恢复友链
    if backup.get("friends"):
        await Friend.all().delete()
        for item in backup["friends"]:
            await Friend.create(**item)

    # 恢复用户
    if backup.get("users"):
        await User.all().delete()
        for item in backup["users"]:
            await User.create(**item)

    await FastAPICache.clear()
    return BaseApiOut(message="数据恢复成功")
