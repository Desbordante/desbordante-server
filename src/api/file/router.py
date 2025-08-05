from fastapi import APIRouter

from src.api.file.routes.upload_file import router as upload_file_router

router = APIRouter()

router.include_router(upload_file_router)
