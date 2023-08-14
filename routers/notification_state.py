from fastapi import (
    APIRouter,
    Response,
    Request, Query,
)
from fastapi.responses import JSONResponse

from db.models import NotificationStateUpdatePayload
from db.notifications import (
    update_notification_state,
    get_notification_state_ids_by_status,
)
from .middleware import admin_only

router = APIRouter(
    prefix="/notification_states",
    tags=["notification_state"],
)


@router.get("/", response_model=list[str])
@admin_only
# pylint: disable=unused-argument
async def get_notification_states(request: Request, read: bool = Query(...)):
    notification_state_ids = await get_notification_state_ids_by_status(read)

    return JSONResponse(content=notification_state_ids)


@router.patch("/{notification_id}")
@admin_only
# pylint: disable=unused-argument
async def update_notification_state_read(request: Request,
                                         notification_id: str,
                                         payload: NotificationStateUpdatePayload):
    await update_notification_state(notification_id, payload.read)
    return Response(status_code=200)
