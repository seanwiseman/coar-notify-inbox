import logging

from fastapi import HTTPException, Request
from functools import wraps

from config import settings

_logger = logging.getLogger(__name__)


def ensure_client_is_admin(request: Request):
    if settings.allowed_admin_origins == set("*"):
        return

    client_ip = request.client.host

    if client_ip not in settings.allowed_admin_origins:
        raise HTTPException(status_code=403, detail="Access forbidden: IP not allowed")


def admin_only(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        ensure_client_is_admin(request)
        return await func(request, *args, **kwargs)

    return wrapper
