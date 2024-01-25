# -*- coding: utf-8 -*-
"""
@author: moxiaoying
@create: 2023/4/4
@description:
"""

import uvicorn
from starlette.responses import RedirectResponse

from core import create_app
from settings import settings

app = create_app()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(settings.DOCS_URL)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=settings.DEBUG)
