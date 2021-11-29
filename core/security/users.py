from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
from typing import Optional
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from core.security import verify_password_or_key
from crud.users import get_user_by_email
from database.db import get_db
from models.token import TokenData
from core.config import get_settings

SECRET_KEY = get_settings().secret_key
ALGORITHM = get_settings().algorithm

# may be you can use the same oauth scheme for both user and app
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/login",
    scopes={"me": "Get information about the current user"}
)


async def authenticate_user(database, email: str, password: str):
    user = await get_user_by_email(database, email)
    if not user:
        return False
    if not verify_password_or_key(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: AsyncIOMotorClient = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(email=email, scopes=token_scopes,)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = await get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
