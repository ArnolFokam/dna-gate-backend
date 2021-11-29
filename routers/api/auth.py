from datetime import timedelta
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_settings
from core.security import get_password_or_key_hash
from crud.users import create_user, get_user_by_email
from database.db import get_db
from core.security.users import authenticate_user, create_access_token
from models.token import Token
from models.user import User
from schemas.user import UserRegister

router = APIRouter(
    prefix="/auth"
)

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().token_expire_minutes


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncIOMotorClient = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "scopes": ["me"],
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register_user(user: UserRegister,
                        db: AsyncIOMotorClient = Depends(get_db)):
    user_exists = await get_user_by_email(db, user.email)

    if user_exists is not None:
        raise HTTPException(status_code=403, detail=f"User with email address {user.email} already exists")
    user.password = get_password_or_key_hash(user.password)
    created_user = await create_user(db, user)
    return created_user
