from datetime import datetime
import os
import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import get_settings
from db.notifications import get_notifications
from routers import inbox_router, notification_state_router

templates = Jinja2Templates(directory="templates")


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
    async def home(request: Request):
        def ppjson(value, indent=2):
            return json.dumps({**value, "updated": value["updated"].isoformat()}, indent=indent)

        def dateparse(value):
            return datetime.fromisoformat(value)

        templates.env.filters['dateparse'] = dateparse
        templates.env.filters["tojson_pretty"] = ppjson
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "notifications": await get_notifications()
            }
        )

    return _app


app = create_app()
