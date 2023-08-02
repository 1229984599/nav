from fastapi.staticfiles import StaticFiles
from fastapi import Request, FastAPI

from fastapi.templating import Jinja2Templates


def register_templates(app: FastAPI):
    templates = Jinja2Templates(directory="template")
    # 前端静态资源挂载
    app.mount("/assets", StaticFiles(directory='template/home/assets'), name="homeAssets")

    @app.get('/')
    def handle_index(request: Request):
        return templates.TemplateResponse("home/index.html", {"request": request})

    @app.get('/list')
    def handle_index(request: Request):
        return templates.TemplateResponse("home/index.html", {"request": request})

    # 后端静态资源挂载
    app.mount("/admin/assets", StaticFiles(directory='template/admin/assets'), name="adminAssets")
    app.mount("/admin/static", StaticFiles(directory='template/admin/static'), name="adminStatic")

    @app.get('/admin/')
    def handle_index(request: Request):
        return templates.TemplateResponse("admin/index.html", {"request": request})

    @app.get('/adminserverConfig.json')
    def handle_index(request: Request):
        return templates.TemplateResponse("admin/serverConfig.json", {"request": request})

# 注册模板
