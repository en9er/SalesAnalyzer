from fastapi import (
    APIRouter,
    FastAPI,
)
from fastapi.responses import JSONResponse

from sales_analyzer.web.api.v1.router import router_v1


def create_app() -> FastAPI:
    application = FastAPI(
        title='sales-analyzer',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
    )

    api_router = APIRouter(prefix='/api')
    api_router.include_router(router_v1)

    application.include_router(api_router)

    return application


fastapi_app = create_app()
