import os
import json
from datetime import datetime
from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    Request,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.models import Notification, NotificationInput
from db.notifications import create_notification, get_notifications, get_notification


INBOX_URL = "http://localhost:8000/inbox/"

app = FastAPI()

origin_white_list = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin_white_list,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

templates = Jinja2Templates(directory="templates")


def get_notification_links(notifications: list[Notification]) -> list[str]:
    return [f"{INBOX_URL}{notification['id']}" for notification in notifications]


@app.get("/")
async def home(request: Request):
    def ppjson(value, indent=2):
        return json.dumps(value, indent=indent)

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


@app.options("/inbox/")
async def read_inbox_options():
    return Response(headers={"Accept-Post": "application/ld+json"})


@app.get("/system/")
async def read_system() -> JSONResponse:
    return JSONResponse(
        headers={"content-type": "application/ld+json"},
        content={
            "@context": "http://www.w3.org/ns/ldp",
            "@id": "https://research-organisation.org/system",
            "inbox": INBOX_URL,
        },
    )


@app.get("/inbox/")
async def read_inbox() -> JSONResponse:
    notifications = await get_notifications()
    return JSONResponse(
        headers={"content-type": "application/ld+json"},
        content={
            "@context": "http://www.w3.org/ns/ldp",
            "@id": INBOX_URL,
            "contains": get_notification_links(notifications)
        },
    )


@app.post("/inbox/")
async def add_notification(notification_input: NotificationInput):
    notification_id = await create_notification(notification_input)
    return Response(
        headers={"Location": f"{INBOX_URL}{notification_id}"},
        status_code=201,
    )


@app.get("/inbox/{notification_id}/", response_model=Notification)
async def read_notification(notification_id: str):
    notification = await get_notification(notification_id)

    if notification:
        return JSONResponse(
            headers={"content-type": "application/ld+json"},
            content=notification,
        )

    raise HTTPException(status_code=404, detail="Notification not found")
