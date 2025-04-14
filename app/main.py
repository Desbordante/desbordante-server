from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from .domain import router as api_router
from .exceptions import BaseAppException

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


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         summary=app.summary,
#         description=app.description,
#         routes=app.routes,
#     )
#     extras = {
#         HTTPApiError.__name__: HTTPApiError.model_json_schema(ref_template=REF_TEMPLATE)
#     }
#     openapi_schema["components"]["schemas"].update(extras)
#     app.openapi_schema = openapi_schema

#     return app.openapi_schema


# app.openapi = custom_openapi


app.include_router(api_router)
