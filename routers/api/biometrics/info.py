import datetime

from fastapi import APIRouter, Security, Depends, HTTPException, UploadFile, File
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse

from core.biometrics.emebddings import verify_embedding_match
from core.biometrics.facial import get_face_embedding, validate_face_input
from core.biometrics.vocal import get_voice_embedding, validate_voice_input
from core.security.biometrics import get_current_user
from crud.biometric_info import get_biometric_info_by_id, insert_biometric_info, update_biometric_info, \
    get_all_biometric_info_by_tenant, delete_biometric_info_by_id
from crud.metrics.biometrics import insert_metrics_usage
from database.db import get_db
from schemas.biometric_info import BiometricInfoInsert, BiometricInfoReturn, MatchResponse
from schemas.user import UserInDB

router = APIRouter(
    prefix="/info"
)


@router.get("/")
async def get_all_biometric_by_tenant(db: AsyncIOMotorClient = Depends(get_db),
                                      current_user: UserInDB = Security(get_current_user)):
    infos = await get_all_biometric_info_by_tenant(db, str(current_user.id))

    infos = [{
        "hasFacial": info.facial is not None,
        "hasVocal": info.vocal is not None,
        "id": str(info.id),
        "tenant_id": str(info.tenant_id),
    } for info in infos]

    return infos


@router.get("/{info_id}", response_model=BiometricInfoReturn)
async def get_biometric_by_id(info_id: str,
                              db: AsyncIOMotorClient = Depends(get_db),
                              current_user: UserInDB = Security(get_current_user)):
    # This route is somehow useless because you
    # don't want to give the embedding to the
    # user but but keep it in case
    info = await get_biometric_info_by_id(db, info_id, str(current_user.id))
    if info is None:
        raise HTTPException(status_code=404, detail="Biometric information not found")
    else:
        info = info.dict()
        info["id"] = str(info["id"])
        info["tenant_id"] = str(info["tenant_id"])
        return info


@router.post("/", response_model=BiometricInfoReturn)
async def add_new_biometric_info(face_image: UploadFile = File(None),
                                 voice_recording: UploadFile = File(None),
                                 db: AsyncIOMotorClient = Depends(get_db),
                                 current_user: UserInDB = Security(get_current_user)):
    if face_image is None and voice_recording is None:
        raise HTTPException(status_code=442, detail=f"either face image or voice recording can be empty but not both")

    info = dict()

    # validate the face and check that the input as valid
    if face_image is not None:
        face_image = validate_face_input(face_image)

    if voice_recording is not None:
        voice_recording = validate_voice_input(voice_recording)

    # get the embedding from the faces
    if face_image is not None:
        info["facial"] = await get_face_embedding(face_image)

    if voice_recording is not None:
        info["vocal"] = await get_voice_embedding(voice_recording)

    info["tenant_id"] = str(current_user.id)

    try:
        created_info = await insert_biometric_info(db, BiometricInfoInsert(**info))
    except ValidationError as e:
        raise RequestValidationError(errors=e.raw_errors)

    created_info = created_info.dict()
    created_info["id"] = str(created_info["id"])
    created_info["tenant_id"] = str(created_info["tenant_id"])

    # replace action with constant for centralization
    await insert_metrics_usage(db,
                               "create",
                               created_info["id"],
                               str(current_user.id),
                               datetime.datetime.utcnow())

    return created_info


@router.post("/verify/face/{info_id}", response_model=MatchResponse)
async def verify_face_biometric_by_id(info_id: str,
                                      face_image: UploadFile = File(...),
                                      db: AsyncIOMotorClient = Depends(get_db),
                                      current_user: UserInDB = Security(get_current_user)):
    face_image = validate_face_input(face_image)

    # get current biometric information
    current_info = await get_biometric_info_by_id(db, info_id, str(current_user.id))
    if current_info is None:
        raise HTTPException(status_code=404, detail="Biometric information not found")
    else:
        current_face = current_info.facial
        incoming_face = await get_face_embedding(face_image)
        results = verify_embedding_match(current_face, incoming_face)

        # replace action with constant for centralization
        await insert_metrics_usage(db,
                                   "verify",
                                   info_id,
                                   str(current_user.id),
                                   datetime.datetime.utcnow())

        return results


@router.post("/verify/voice/{info_id}", response_model=MatchResponse)
async def verify_voice_biometric_by_id(info_id: str,
                                       voice_recording: UploadFile = File(...),
                                       db: AsyncIOMotorClient = Depends(get_db),
                                       current_user: UserInDB = Security(get_current_user)):
    voice_recording = validate_voice_input(voice_recording)

    # get current biometric information
    current_info = await get_biometric_info_by_id(db, info_id, str(current_user.id))
    if current_info is None:
        raise HTTPException(status_code=404, detail="Biometric information not found")
    else:
        current_voice = current_info.vocal
        incoming_voice = await get_voice_embedding(voice_recording)
        results = verify_embedding_match(current_voice, incoming_voice)

        # replace action with constant for centralization
        # TODO: find a way to log the event when the verification was successful or failed
        await insert_metrics_usage(db,
                                   "verify",
                                   info_id,
                                   str(current_user.id),
                                   datetime.datetime.utcnow())

        return results


@router.put("/{info_id}")
async def update_existing_biometric_info(info_id: str,
                                         face_image: UploadFile = File(None),
                                         voice_recording: UploadFile = File(None),
                                         db: AsyncIOMotorClient = Depends(get_db),
                                         current_user: UserInDB = Security(get_current_user)):
    info = dict()

    # validate the face and check that the input as valid
    if face_image is not None:
        face_image = validate_face_input(face_image)

    if voice_recording is not None:
        voice_recording = validate_voice_input(voice_recording)

    # get the embedding from th faces
    if face_image is not None:
        info["facial"] = await get_face_embedding(face_image)

    if voice_recording is not None:
        info["vocal"] = await get_voice_embedding(voice_recording)

    info["tenant_id"] = current_user.id

    try:
        updated_info = await update_biometric_info(db, info_id, BiometricInfoInsert(**info))
    except ValidationError as e:
        raise RequestValidationError(errors=e.raw_errors)

    if updated_info is None:
        raise HTTPException(status_code=304, detail="could not update the biometric info")

    updated_info = updated_info.dict()
    updated_info["id"] = str(updated_info["id"])
    updated_info["tenant_id"] = str(updated_info["tenant_id"])

    # replace action with constant for centralization
    await insert_metrics_usage(db,
                               "update",
                               updated_info["id"],
                               updated_info["tenant_id"],
                               datetime.datetime.utcnow())

    return updated_info


@router.delete("/{info_id}", response_model=BiometricInfoReturn)
async def delete_biometric_by_id(info_id: str,
                                 db: AsyncIOMotorClient = Depends(get_db),
                                 current_user: UserInDB = Security(get_current_user)):
    delete_result = await delete_biometric_info_by_id(db, info_id, str(current_user.id))
    if delete_result is not None:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Biometric info with {info_id} not found")
