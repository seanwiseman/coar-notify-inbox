from datetime import datetime
import os
import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Query

from config import get_settings, PAGE_LIMIT
from db.notifications import get_notifications, get_notifications_collection
from routers import inbox_router, notification_state_router

templates = Jinja2Templates(directory="templates")
templates.env.globals['max'] = max
templates.env.globals['min'] = min


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.mount("/static",
               StaticFiles(directory=os.path.join(os.path.dirname(__file__),
                                                  "static")), name="static")

    _app.include_router(inbox_router)
    _app.include_router(notification_state_router)

    @_app.get("/")
    async def home(request: Request, page: int = Query(1, ge=1),
                   page_size: int = Query(PAGE_LIMIT, ge=1)):
        def ppjson(value, indent=2):
            return json.dumps({**value, "updated": value["updated"].isoformat()}, indent=indent)

        def dateparse(value):
            return datetime.fromisoformat(value)

        templates.env.filters['dateparse'] = dateparse
        templates.env.filters["tojson_pretty"] = ppjson

        notifications = await get_notifications(page=page, page_size=page_size)
        collection = await get_notifications_collection()
        total_notifications = await collection.count_documents({})
        total_pages = (total_notifications + page_size - 1) // page_size

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "notifications": notifications,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        )

    return _app


app = create_app()
