import uuid
from datetime import datetime

from pymongo import DESCENDING

from db import get_db, get_collection
from db.models import Notification, NotificationInput


COLLECTION_NAME = "notifications"
PAGE_LIMIT = 100


async def _get_collection():
    db = await get_db()
    return await get_collection(db, COLLECTION_NAME)


async def create_notification(notification_input: NotificationInput) -> str:
    collection = await _get_collection()

    notification = {
        "received_at": datetime.utcnow().isoformat(),
        **notification_input,
    }

    await collection.insert_one(notification)
    return notification["id"]


async def get_notification(notification_id: str) -> Notification:
    collection = await _get_collection()
    notification = await collection.find_one({"id": notification_id}, {"_id": 0})
    return notification


async def get_notifications() -> list[Notification]:
    collection = await _get_collection()
    notifications = await collection\
        .find({}, {"_id": 0})\
        .sort("received_at", DESCENDING)\
        .to_list(length=PAGE_LIMIT)
    return notifications


async def delete_notification(notification_id: uuid.UUID) -> None:
    collection = await _get_collection()
    await collection.delete_one({"id": notification_id})
