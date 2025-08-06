from fastapi import APIRouter

from src.api.dataset.routes.upload_dataset import router as upload_dataset_router

router = APIRouter()

router.include_router(upload_dataset_router)
