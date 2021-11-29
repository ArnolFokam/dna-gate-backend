from fastapi import APIRouter, Security
from core.security.users import get_current_user
from models.user import User

router = APIRouter(
    prefix="/users"
)


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Security(get_current_user, scopes=["me"])):
    return current_user
