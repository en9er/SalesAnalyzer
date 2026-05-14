from fastapi import APIRouter

from sales_analyzer.web.api.v1.sales_analyzer import router as sales_analyzer_router

router_v1 = APIRouter(prefix='/v1')
router_v1.include_router(sales_analyzer_router)
