from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_settings
from models.base_object_id import BaseObjectId
from models.biometrics.info import BiometricInfo
from schemas.biometric_info import BiometricInfoInDB, BiometricInfoInsert

collection_name = "biometric_infos"
database = get_settings().database


async def get_biometric_info_by_id(db: AsyncIOMotorClient,
                                   info_id: str,
                                   tenant_id: str):
    info = await db[database][collection_name].find_one({"_id": BaseObjectId(info_id),
                                                         "tenant_id": BaseObjectId(tenant_id)})
    if info is not None:
        return BiometricInfoInDB(**info)


async def get_all_biometric_info_by_tenant(db: AsyncIOMotorClient,
                                           tenant_id: str):
    infos = await db[database][collection_name].find({"tenant_id": BaseObjectId(tenant_id)}).to_list(length=1000)
    return [BiometricInfoInDB(**info) for info in infos]


async def get_total_biometric_infos(db: AsyncIOMotorClient,
                                    tenant_id: str):
    infos = await get_all_biometric_info_by_tenant(db, tenant_id)
    return len(infos)


async def get_total_biometric_infos_by_type(db: AsyncIOMotorClient,
                                            _type: str,
                                            tenant_id: str):
    infos = await db[database][collection_name].find({
        "tenant_id": BaseObjectId(tenant_id),
        _type: {"$ne": None}
    }).to_list(length=1000)

    infos = [BiometricInfoInDB(**info) for info in infos]
    return len(infos)


async def insert_biometric_info(db: AsyncIOMotorClient,
                                info: BiometricInfoInsert):
    info = info.dict()
    new_info = await db[database][collection_name].insert_one(info)
    created_info = await db[database][collection_name].find_one({"_id": new_info.inserted_id})
    if created_info is not None:
        return BiometricInfoInDB(**created_info)


async def update_biometric_info(db: AsyncIOMotorClient,
                                _id: str,
                                info: BiometricInfo):
    info = {k: v for k, v in info.dict().items() if v is not None}

    if len(info.keys()) >= 1:
        update_result = await db[database][collection_name].update_one({"_id": BaseObjectId(_id)},
                                                                       {"$set": info})

        if update_result.modified_count == 1:
            if (updated_info := await db[database][collection_name].find_one({"_id": BaseObjectId(_id)})) is not None:
                return BiometricInfoInDB(**updated_info)
