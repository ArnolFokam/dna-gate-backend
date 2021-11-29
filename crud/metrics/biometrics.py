import logging

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic.schema import datetime

from core.config import get_settings
from models.base_object_id import BaseObjectId

collection_name = "biometrics_infos_metrics"
database = get_settings().database


async def insert_metrics_usage(db: AsyncIOMotorClient,
                               action: str,
                               info_id: str,
                               tenant_id: str,
                               timestamp: datetime):
    if action not in ["verify", "create", "update"]:
        logging.error(f"Unidentified action { {action} } for biometric metrics")
        raise HTTPException(status_code=500, detail="unknown action")

    await db[database][collection_name].insert_one({
        "metadata": {
            "tenant_id": BaseObjectId(tenant_id),
            "info_id": BaseObjectId(info_id),
            "action": action
        },
        "ts": timestamp
    })


async def get_action_history(db: AsyncIOMotorClient,
                             action: str,
                             tenant_id: str):
    if action not in ["verify", "create", "update"]:
        logging.error(f"Unidentified action { {action} } for biometric metrics")
        raise HTTPException(status_code=500, detail="unknown action")

    results = await db[database][collection_name].find({
        "metadata.tenant_id": BaseObjectId(tenant_id),
        "metadata.action": action,
    }).to_list(length=1000)

    return list(map(lambda x: x['ts'].strftime("%Y-%m-%d %H:%M:%S"), results))


async def get_total_number_of_actions(db: AsyncIOMotorClient,
                                      action: str,
                                      tenant_id: str):
    results = await db[database][collection_name].find({
        "metadata.tenant_id": BaseObjectId(tenant_id),
        "metadata.action": action,
    }).to_list(length=1000)

    return len(results)
