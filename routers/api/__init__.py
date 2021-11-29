from fastapi import APIRouter

from routers.api import auth, users
from routers.api import biometrics

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(biometrics.router)
