from motor.motor_asyncio import AsyncIOMotorClient

from config import get_settings


async def get_db():
    if get_settings().mongo_db_uri:
        client = AsyncIOMotorClient(get_settings().mongo_db_uri)
        return client.notification_store

    return None


async def get_collection(collection_name: str):
    database = await get_db()
    return database[collection_name]
