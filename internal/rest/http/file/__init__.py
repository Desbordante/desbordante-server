from fastapi import APIRouter

from internal.rest.http.file.upload_csv_dataset import router as upload_csv_file_router

router = APIRouter(prefix="/file", tags=["file"])

router.include_router(upload_csv_file_router)
