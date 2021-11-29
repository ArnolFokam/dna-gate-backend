from pydantic import Field

from models.base_object_id import BaseObjectId
from models.user import User


class UserRegister(User):
    password: str = Field(...)

    class Config:
        json_encoders = {BaseObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "secret"
            }
        }


class UserInDB(User):
    id: BaseObjectId = Field(..., alias="_id")
    apiKey: str = Field(...)
    password: str = Field(...)


class UserLogin:
    email: str = Field(...)
    password: str = Field(...)
