from typing import List

from pydantic import BaseModel


class UsageHistory(BaseModel):
    verifications: List[str]
    updates: List[str]
    creations: List[str]


class TotalUsage(BaseModel):
    biometric_infos: int
    verifications: int
    creations: int
    updates: int


class BiometricInfosRatio(BaseModel):
    face: int
    voice: int
