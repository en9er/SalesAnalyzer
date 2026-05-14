from pydantic import BaseModel, Field
from typing import List
from sales_analyzer.web.api.schemas.common import SaleUnit
from sales_analyzer.web.services.sales_analyzer import DishMargin

class AnalyzeResultResponse(BaseModel):
    top_margin_dishes: List[DishMargin] = Field(description='Топ блюд по маржинальности')
    loss_making: List[DishMargin] = Field(description='Блюда с маржой ниже n', default_factory=list)
    total_revenue: float = Field(description='Общее ревеню')
    total_margin: float = Field(description='Общая маржинальность')
    suggestions: List[str] = Field(description='Рекомендации', default_factory=list)
