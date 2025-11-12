from fastapi import APIRouter

from src.api.public.routes.get_public_datasets import (
    router as get_public_datasets_router,
)
from src.api.public.routes.upload_public_dataset import (
    router as upload_public_dataset_router,
)

router = APIRouter()

router.include_router(get_public_datasets_router, prefix="/datasets", tags=["public"])
router.include_router(upload_public_dataset_router, prefix="/datasets", tags=["public"])
