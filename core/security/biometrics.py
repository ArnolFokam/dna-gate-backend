from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from starlette import status

from core.config import get_settings
from crud.keys import get_user_api_key
from database.db import get_db

ALGORITHM = get_settings().algorithm
API_KEY_NAME = get_settings().api_key_name

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
api_key_header = APIKeyHeader(name=API_KEY_NAME,  scheme_name="API key header", auto_error=False)


async def get_current_user(api_key: str = Security(api_key_header),  db: AsyncIOMotorClient = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f"Api-Key"},
    )

    user = await get_user_api_key(db, api_key)
    if user is None:
        raise credentials_exception

    return user
