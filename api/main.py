# -*- coding: utf-8 -*-
"""
@author: xingxingzaixian
@create: 2021/4/4
@description:
"""

import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse

from core.server import create_app
from settings import settings

app = create_app()


@app.get('/')
def handle_index():
    return RedirectResponse(settings.DOCS_URL)


@app.get(settings.DOCS_URL, include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, reload=settings.DEBUG, loop="asyncio")
