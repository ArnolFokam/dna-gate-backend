from pydantic import Field, BaseModel

from models.biometrics.info import BiometricInfo
from models.base_object_id import BaseObjectId


class BiometricInfoInsert(BiometricInfo):
    tenant_id:  BaseObjectId = Field(..., alias="tenant_id")


class BiometricInfoInDB(BiometricInfo):
    id: BaseObjectId = Field(..., alias="_id")
    tenant_id:  BaseObjectId = Field(..., alias="tenant_id")


class BiometricInfoReturn(BaseModel):
    id:  str = Field(...)


class MatchResponse(BaseModel):
    match: bool
    distance: float
    metric: str
    threshold: float
