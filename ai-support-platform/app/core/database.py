from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI)

async def close_mongo_connection():
    db.client.close()

def get_database():
    return db.client[settings.DATABASE_NAME]

async def init_db():
    if db.client is None:
        await connect_to_mongo()

async def close_db():
    if db.client:
        db.client.close()