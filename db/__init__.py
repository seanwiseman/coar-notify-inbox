from motor.motor_asyncio import AsyncIOMotorClient

from config import settings


async def get_db():
    client = AsyncIOMotorClient(settings.mongo_db_uri)
    return client.notification_store


async def get_collection(database, collection_name: str):
    return database[collection_name]
