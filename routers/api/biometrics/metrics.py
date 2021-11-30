from fastapi import Security, Depends
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from core.security.users import get_current_user
from crud.biometric_info import get_total_biometric_infos, get_total_biometric_infos_by_type
from crud.metrics.biometrics import get_action_history, get_total_number_of_actions
from database.db import get_db
from models.biometrics.metrics import UsageHistory, TotalUsage, BiometricInfosRatio
from schemas.user import UserInDB

router = APIRouter(
    prefix="/metrics"
)


@router.get("/usage-history", response_model=UsageHistory)
async def get_metrics(db: AsyncIOMotorClient = Depends(get_db),
                      user: UserInDB = Security(get_current_user)):
    verifications_history = await get_action_history(db, "verify", str(user.id))
    creations_history = await get_action_history(db, "create", str(user.id))
    updates_history = await get_action_history(db, "update", str(user.id))

    return {
        "verifications": verifications_history,
        "updates": updates_history,
        "creations": creations_history
    }


@router.get("/total-usage", response_model=TotalUsage)
async def get_total_usage(db: AsyncIOMotorClient = Depends(get_db),
                          user: UserInDB = Security(get_current_user)):
    total_biometric_infos = await get_total_biometric_infos(db, str(user.id))
    total_create_actions = await get_total_number_of_actions(db, "create", str(user.id))
    total_verify_actions = await get_total_number_of_actions(db, "verify", str(user.id))
    total_update_actions = await get_total_number_of_actions(db, "update", str(user.id))

    return {
        "biometric_infos": total_biometric_infos,
        "creations": total_create_actions,
        "verifications": total_verify_actions,
        "updates": total_update_actions
    }


@router.get("/infos-ratio", response_model=BiometricInfosRatio)
async def get_biometric_infos_ratio(db: AsyncIOMotorClient = Depends(get_db),
                                    user: UserInDB = Security(get_current_user)):

    total_face_infos = await get_total_biometric_infos_by_type(db, "facial", str(user.id))
    total_voice_infos = await get_total_biometric_infos_by_type(db, "vocal", str(user.id))

    return {
        "face": total_face_infos,
        "voice": total_voice_infos
    }
