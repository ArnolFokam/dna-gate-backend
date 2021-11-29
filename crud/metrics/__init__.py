import logging
from pymongo.errors import CollectionInvalid

from crud.metrics.biometrics import collection_name as biometrics_metrics_collection

from core.config import get_settings

collections = [biometrics_metrics_collection]
database = get_settings().database


async def setup_metrics_collection(db):
    """
    timeseries={
        "timeField": "ts",
        "metaField": "metadata",
        "granularity": "hours"
    },
    expireAfterSeconds=15552000  # six months
    """
    for collection_name in collections:
        try:
            await db[database].create_collection(collection_name)
        except CollectionInvalid:
            logging.info(f"{collection_name} collection is already in the database.")
