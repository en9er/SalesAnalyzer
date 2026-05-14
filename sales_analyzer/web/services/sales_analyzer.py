from typing import List, Tuple

from pydantic import BaseModel
from sales_analyzer.core.calculator import calculate_margin, calculate_revenue, calculate_cost
from sales_analyzer.web.api.schemas.common import SaleUnit
from sales_analyzer.infrastructure.config import config


DishMargin = Tuple[str, float]
DishQuantity = Tuple[str, int]

class SalesAnalyzeData(BaseModel):
    dish_top_margin: List[DishMargin]
    dish_top_sales_quantity: List[DishQuantity]
    loss_making: List[DishMargin]
    total_revenue: float
    total_margin: float


class SalesAnalyzerService:
    @staticmethod
    def calculate_top_margin_dishes(sales_info: List[SaleUnit]) -> List[DishMargin]:
        top_margin: List[DishMargin] = list()
        for sale in sales_info:
            top_margin.append((sale.dish, calculate_margin(sale.cost_price, sale.selling_price)))
        top_margin.sort(key=lambda x: x[1], reverse=True)
        return top_margin
    
    @staticmethod
    def calculate_top_sale_quantity_dishes(sales_info: List[SaleUnit]) -> List[DishMargin]:
        top_quantity: List[DishMargin] = list()
        for sale in sales_info:
            top_quantity.append((sale.dish, sale.quantity))
        top_quantity.sort(key=lambda x: x[1], reverse=True)
        return top_quantity
    
    @staticmethod
    def get_loss_making(dish_margin_info: List[DishMargin]) -> List[DishMargin]:
        """
        Поиск немаржинальных блюд.

        Проходимся по отсортированному(по убыванию) массиву маржинальности товаров
        и возвращаем немаржинальные
        """
        for i, (_, margin) in enumerate(dish_margin_info):
            # Как только встретили маржинальность меньше 30 сразу возвращаем весь оставшийся
            # массив, так как он отсортирован и дальше будет только меньше  
            if margin < config.ANALYZER_CONFIG.LOSS_MAKING_MARGIN_THRESHOLD:
                return dish_margin_info[i:]
        return []

    @staticmethod
    def total_revenue(sales_info: List[SaleUnit]):
        revenue_info: List[Tuple[float, int]] = list()
        for sale_info in sales_info:
            revenue_info.append((sale_info.selling_price, sale_info.quantity))

        return calculate_revenue(revenue_info)

    @staticmethod
    def calculate_total_cost(sales_info: List[SaleUnit]):
        cost_info: List[Tuple[float, int]] = list()
        for sale_info in sales_info:
            cost_info.append((sale_info.cost_price, sale_info.quantity))

        return calculate_cost(cost_info)
    
    @staticmethod
    def total_margin(total_revenue: float, total_cost: float):
        return total_revenue - total_cost
    
    def analyze_sales(self, sales_info: List[SaleUnit]):
        dish_top_margin = self.calculate_top_margin_dishes(sales_info)
        dish_top_sales_quantity = self.calculate_top_sale_quantity_dishes(sales_info)
        loss_making = self.get_loss_making(dish_top_margin)
        total_revenue = self.total_revenue(sales_info)
        total_cost = self.calculate_total_cost(sales_info)
        total_margin = self.total_margin(total_revenue, total_cost)

        return SalesAnalyzeData(
            dish_top_margin=dish_top_margin,
            dish_top_sales_quantity=dish_top_sales_quantity,
            loss_making=loss_making,
            total_revenue=total_revenue,
            total_margin=total_margin
        )
