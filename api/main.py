# -*- coding: utf-8 -*-
"""
@author: moxiaoying
@create: 2023/4/4
@description:
"""

import uvicorn
from starlette.responses import RedirectResponse

from fastapi.openapi.docs import get_swagger_ui_html

from core import create_app
from settings import settings

app = create_app()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(settings.DOCS_URL)


@app.get(settings.DOCS_URL, include_in_schema=False)
async def custom_swagger_ui_html():
    """
    重写文档cdn为国内，防止链接被墙
    :return:
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=settings.DEBUG)
