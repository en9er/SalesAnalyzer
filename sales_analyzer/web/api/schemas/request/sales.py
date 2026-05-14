from pydantic import BaseModel, Field
from typing import List

from sales_analyzer.web.api.schemas.common import SaleUnit


class SalesListRequest(BaseModel):
    sales: List[SaleUnit] = Field(default_factory=list)
