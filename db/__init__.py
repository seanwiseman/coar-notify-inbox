import os

from motor.motor_asyncio import AsyncIOMotorClient


DB_URI = os.getenv("DB_URI")


async def get_db():
    client = AsyncIOMotorClient(DB_URI)
    return client.notification_store


async def get_collection(db, collection_name: str):
    return db[collection_name]


