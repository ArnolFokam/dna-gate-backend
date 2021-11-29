import uuid

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_settings
from schemas.user import UserInDB

collection_name = "users"
database = get_settings().database


async def get_user_api_key(db: AsyncIOMotorClient,
                           apiKey: str):
    user = await db[database][collection_name].find_one({"apiKey": apiKey})
    if user is not None:
        return UserInDB(**user)


async def renew_api_key(db: AsyncIOMotorClient,
                        apiKey: str):
    key = str(uuid.uuid4())
    await db[database][collection_name].update_one({"apiKey": apiKey},
                                                   {"$set": {"apiKey": key}})
    updated_user = await db[database][collection_name].find_one({"apiKey": key})
    return updated_user['apiKey']
