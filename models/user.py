from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class User(BaseModel):
    first_name: str = Field(...,
                            min_length=2,
                            max_length=50)
    last_name: str = Field(...,
                           min_length=2,
                           max_length=50)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
            }
        }
