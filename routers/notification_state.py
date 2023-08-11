from fastapi import (
    APIRouter,
    Response,
    Request,
)

from db.models import NotificationStateUpdatePayload
from db.notifications import update_notification_state
from .middleware import admin_only

router = APIRouter(
    prefix="/notification_state",
    tags=["notification_state"],
)


@router.patch("/{notification_id}")
@admin_only
# pylint: disable=unused-argument
async def update_notification_state_read(request: Request,
                                         notification_id: str,
                                         payload: NotificationStateUpdatePayload):
    await update_notification_state(notification_id, payload.read)
    return Response(status_code=200)
