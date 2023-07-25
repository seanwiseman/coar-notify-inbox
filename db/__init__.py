from motor.motor_asyncio import AsyncIOMotorClient

DB_NAME = "notification_store"
DB_USER = "root"
DB_PASSWORD = "password"
DB_PORT = 27017
DB_HOST = "localhost"

DB_URI = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"


async def get_db():
    client = AsyncIOMotorClient(DB_URI)
    return client.notification_store


async def get_collection(db, collection_name: str):
    return db[collection_name]


