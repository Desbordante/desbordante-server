from fastapi import APIRouter
from .ping import router as ping_router
from .task import router as task_router
from .dataset import router as dataset_router

router = APIRouter(prefix="/api")
router.include_router(ping_router)
router.include_router(task_router)
router.include_router(dataset_router)
