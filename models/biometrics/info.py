from typing import List, Optional

from pydantic import validator
from pydantic.main import BaseModel


class BiometricInfo(BaseModel):
    facial: Optional[List[float]]
    vocal: Optional[List[float]]

    @validator('facial')
    def facial_embedding_must_have_correct_length(cls, v):
        if len(v) != 512:
            raise ValueError('must be a 512-D vector embedding')
        return v

    @validator('vocal')
    def voice_embedding_must_have_correct_length(cls, v):
        if v is not None and len(v) != 2048:
            raise ValueError('must be a 512-D vector embedding')
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "facial": "[]",  # facial example
                "vocal": "[]",  # vocal example
            }
        }
