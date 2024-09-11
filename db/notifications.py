import uuid

from pymongo import DESCENDING

from config import PAGE_LIMIT
from db import get_collection
from db.models import Notification


NOTIFICATIONS_COLLECTION_NAME = "notifications"
NOTIFICATION_STATES_COLLECTION_NAME = "notification_states"


class FailedToFindNotificationState(Exception):
    pass


async def get_notifications_collection():
    return await get_collection(NOTIFICATIONS_COLLECTION_NAME)


async def get_notification_states_collection():
    return await get_collection(NOTIFICATION_STATES_COLLECTION_NAME)


async def create_notification(notification: Notification) -> str:
    notification_collection = await get_notifications_collection()
    notification_states_collection = await get_notification_states_collection()
    await notification_collection.insert_one(notification.model_dump(by_alias=True))
    await notification_states_collection.insert_one({"id": notification.id, "read": False})

    return notification.id


async def get_notification(notification_id: str) -> Notification:
    collection = await get_notifications_collection()
    notification = await collection.find_one({"id": notification_id}, {"_id": 0})
    return notification


async def get_notifications(page: int = 1, page_size: int = PAGE_LIMIT) -> list[Notification]:
    collection = await get_notifications_collection()
    skip = (page - 1) * page_size
    notifications = await collection \
        .find({}, {"_id": 0}) \
        .sort("updated", DESCENDING) \
        .skip(skip) \
        .limit(page_size) \
        .to_list(length=page_size)
    return notifications


async def delete_notification(notification_id: uuid.UUID) -> None:
    collection = await get_notifications_collection()
    await collection.delete_one({"id": notification_id})


async def get_notification_state_ids_by_status(read: bool) -> list[str]:
    collection = await get_notification_states_collection()
    notification_states = await collection \
        .find({"read": read}, {"_id": 0}) \
        .to_list(length=PAGE_LIMIT)
    return [state["id"] for state in notification_states]


async def update_notification_state(notification_id: str, read: bool) -> None:
    collection = await get_notification_states_collection()
    result = await collection.update_one({"id": notification_id}, {"$set": {"read": read}})

    if result.matched_count == 0:
        raise FailedToFindNotificationState(f"Could not find notification state for "
                                            f"notification {notification_id}")
