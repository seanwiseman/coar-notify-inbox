from datetime import datetime
import os
import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.notifications import get_notifications
from routers import inbox_router


origin_white_list = ["*"]

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin_white_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static",
          StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.include_router(inbox_router)


@app.get("/")
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
