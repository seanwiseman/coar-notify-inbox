import uuid

from pymongo import DESCENDING

from db import get_db, get_collection
from db.models import Notification


NOTIFICATIONS_COLLECTION_NAME = "notifications"
NOTIFICATION_STATES_COLLECTION_NAME = "notification_states"
PAGE_LIMIT = 100


async def _get_notifications_collection():
    database = await get_db()
    return await get_collection(database, NOTIFICATIONS_COLLECTION_NAME)


async def _get_notification_states_collection():
    database = await get_db()
    return await get_collection(database, NOTIFICATION_STATES_COLLECTION_NAME)


async def create_notification(notification: Notification) -> str:
    notification_collection = await _get_notifications_collection()
    notification_states_collection = await _get_notification_states_collection()
    await notification_collection.insert_one(notification.model_dump(by_alias=True))
    await notification_states_collection.insert_one({"id": notification.id, "read": False})

    return notification.id


async def get_notification(notification_id: str) -> Notification:
    collection = await _get_notifications_collection()
    notification = await collection.find_one({"id": notification_id}, {"_id": 0})
    return notification


async def get_notifications() -> list[Notification]:
    collection = await _get_notifications_collection()
    notifications = await collection\
        .find({}, {"_id": 0})\
        .sort("updated", DESCENDING)\
        .to_list(length=PAGE_LIMIT)
    return notifications


async def delete_notification(notification_id: uuid.UUID) -> None:
    collection = await _get_notifications_collection()
    await collection.delete_one({"id": notification_id})
