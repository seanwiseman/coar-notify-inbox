from fastapi import (
    APIRouter,
    HTTPException,
    Response,
)
from fastapi.responses import JSONResponse

from db.models import Notification
from db.notifications import create_notification, get_notifications, get_notification
from validation.validate import validate_notification


router = APIRouter(
    prefix="/inbox",
    tags=["inbox"],
)

INBOX_URL = "http://localhost:8000/inbox/"


def get_notification_links(notifications: list[Notification]) -> list[str]:
    return [f"{INBOX_URL}{notification['id']}" for notification in notifications]


@router.options("/")
async def read_inbox_options():
    return Response(headers={"Accept-Post": "application/ld+json"})


@router.get("/")
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


@router.post("/")
async def add_notification(notification: Notification):
    conforms, errors = validate_notification(notification)

    if not conforms:
        raise HTTPException(status_code=400, detail=errors)

    notification_id = await create_notification(notification)
    return Response(
        headers={"Location": f"{INBOX_URL}{notification_id}"},
        status_code=201,
    )


@router.get("/{notification_id}/", response_model=Notification)
async def read_notification(notification_id: str):
    notification = await get_notification(notification_id)

    if notification:
        return JSONResponse(
            headers={"content-type": "application/ld+json"},
            content=notification,
        )

    raise HTTPException(status_code=404, detail="Notification not found")
