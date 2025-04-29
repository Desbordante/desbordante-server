from fastapi import APIRouter

from src.api.file.routes.get_datasets import router as get_datasets_router
from src.api.file.routes.upload_dataset import router as upload_dataset_router

router = APIRouter()

router.include_router(upload_dataset_router)
router.include_router(get_datasets_router)
