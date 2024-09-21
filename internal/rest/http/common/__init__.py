from fastapi import APIRouter

from internal.rest.http.common.ping import router as ping_router

router = APIRouter(prefix="/common", tags=["common"])

router.include_router(ping_router)
