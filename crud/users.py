import uuid
from typing import Union

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_settings
from models.base_object_id import BaseObjectId
from schemas.user import UserInDB, UserRegister

collection_name = "users"
database = get_settings().database


async def get_user_by_id(db: AsyncIOMotorClient,
                         user_id: str):
    user = await db[database][collection_name].find_one({"_id": BaseObjectId(user_id)})
    if user is not None:
        return UserInDB(**user)


async def get_user_by_email(db: AsyncIOMotorClient,
                            email: str):
    user = await db[database][collection_name].find_one({"email": email})
    if user is not None:
        return UserInDB(**user)


async def create_user(db: AsyncIOMotorClient,
                      user: Union[UserRegister]):
    user = jsonable_encoder(user)

    # create an api key, (note: should make a separate
    # storage for that with dedicated fields for scopes etc)
    user['apiKey'] = str(uuid.uuid4())

    new_user = await db[database][collection_name].insert_one(user)
    created_user = await db[database][collection_name].find_one({"_id": new_user.inserted_id})
    return UserInDB(**created_user)
