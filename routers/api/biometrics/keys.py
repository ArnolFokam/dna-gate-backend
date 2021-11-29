from fastapi import Depends, Security
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from crud.keys import renew_api_key
from database.db import get_db
from core.security.users import get_current_user
from models.biometrics.keys import ApiKey
from schemas.user import UserInDB

router = APIRouter(
    prefix="/keys"
)


@router.get("/", response_model=ApiKey)
async def get_api_key(current_user: UserInDB = Security(get_current_user)):
    return {"api_key": current_user.apiKey}


@router.put("/renew", response_model=ApiKey)
async def request_new_api_key(db: AsyncIOMotorClient = Depends(get_db),
                              current_user: UserInDB = Security(get_current_user)):
    key = await renew_api_key(db, current_user.apiKey)
    return {"api_key": key}
