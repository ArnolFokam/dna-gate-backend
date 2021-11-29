from fastapi import APIRouter

from routers.api.biometrics import keys, metrics, info

router = APIRouter(prefix="/biometrics")
router.include_router(keys.router)
router.include_router(metrics.router)
router.include_router(info.router)
