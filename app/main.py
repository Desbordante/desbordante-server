from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .exceptions import BaseAppException


from .domain import router as api_router

app = FastAPI(generate_unique_id_function=lambda route: route.name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(BaseAppException)
def app_exception_handler(request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(api_router)
