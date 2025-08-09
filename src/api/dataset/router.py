from fastapi import APIRouter

from src.api.dataset.routes.delete_dataset import router as delete_dataset_router
from src.api.dataset.routes.get_dataset import router as get_dataset_router
from src.api.dataset.routes.get_datasets import router as get_datasets_router
from src.api.dataset.routes.upload_dataset import router as upload_dataset_router

router = APIRouter()

router.include_router(upload_dataset_router)
router.include_router(get_datasets_router)
router.include_router(get_dataset_router)
router.include_router(delete_dataset_router)
