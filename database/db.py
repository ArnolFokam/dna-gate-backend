from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings
from crud.metrics import setup_metrics_collection


class DataBase:
    client: AsyncIOMotorClient = None


database = DataBase()


async def get_db() -> AsyncIOMotorClient:
    """Return database client instance."""
    return database.client


async def connect_db():
    """Create database connection."""
    database.client = AsyncIOMotorClient(get_settings().mongodb_url)
    await setup_metrics_collection(database.client)


async def close_db():
    """Close database connection."""
    database.client.close()
