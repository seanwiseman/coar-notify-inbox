import json
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Request,
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


def get_inbox_url(request: Request) -> str:
    return str(request.base_url) + "inbox/"


def get_notification_links(notifications: list[Notification], base_url: str) -> list[str]:
    return [f"{base_url}{notification['id']}" for notification in notifications]


@router.options("/")
async def read_inbox_options():
    return Response(headers={"Accept-Post": "application/ld+json"})


@router.get("/")
async def read_inbox(request: Request) -> JSONResponse:
    inbox_url = get_inbox_url(request)
    notifications = await get_notifications()

    return JSONResponse(
        headers={"content-type": "application/ld+json"},
        content={
            "@context": "http://www.w3.org/ns/ldp",
            "@id": inbox_url,
            "contains": get_notification_links(notifications, base_url=inbox_url),
        },
    )


@router.post("/")
async def add_notification(request: Request, payload: dict = Body(...)):
    conforms, errors = validate_notification(payload)

    if not conforms:
        raise HTTPException(status_code=400, detail=errors)

    notification_id = await create_notification(Notification(**payload))
    return Response(
        headers={"Location": f"{get_inbox_url(request)}{notification_id}"},
        status_code=201,
    )


@router.get("/{notification_id}/", response_model=Notification)
async def read_notification(notification_id: str):
    notification = await get_notification(notification_id)

    if notification:
        return Response(
            headers={"content-type": "application/ld+json"},
            content=json.dumps(notification, default=str),
        )

    raise HTTPException(status_code=404, detail="Notification not found")
