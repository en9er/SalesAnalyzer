import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sales_analyzer.core.services.suggestions import ISuggestionsService
from sales_analyzer.web.api.schemas.request.sales import SalesListRequest
from sales_analyzer.web.api.schemas.response.analyze import AnalyzeResultResponse
from sales_analyzer.web.services.sales_analyzer import SalesAnalyzeData, SalesAnalyzerService
from sales_analyzer.infrastructure.config import config
from sales_analyzer.web.services.suggestions import get_suggestions_service

router = APIRouter(tags=['Sales'])


@router.post('/analyze_sales')
async def analyze_sales(
    sales_info: SalesListRequest,
    sales_analyzer_service: SalesAnalyzerService = Depends(),
    suggestions_service: ISuggestionsService = Depends(get_suggestions_service),
) -> AnalyzeResultResponse:
    sales_analyze_data: SalesAnalyzeData = sales_analyzer_service.analyze_sales(sales_info.sales)
    
    suggestions = suggestions_service.get_suggestions(sales_analyze_data.dish_top_margin, sales_analyze_data.dish_top_sales_quantity)
    
    return AnalyzeResultResponse(
        top_margin_dishes=sales_analyze_data.dish_top_margin[:3],
        loss_making=sales_analyze_data.loss_making,
        total_revenue=sales_analyze_data.total_revenue,
        total_margin=sales_analyze_data.total_margin,
        suggestions=suggestions
    )
