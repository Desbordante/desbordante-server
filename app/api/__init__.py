from fastapi import APIRouter
from .ping import router as ping_router

router = APIRouter(prefix="/api")
router.include_router(ping_router)
