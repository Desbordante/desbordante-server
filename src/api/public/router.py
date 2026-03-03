from fastapi import APIRouter

from src.api.public.routes.get_public_datasets import (
    router as get_public_datasets_router,
)

router = APIRouter()

router.include_router(get_public_datasets_router, prefix="/datasets")
