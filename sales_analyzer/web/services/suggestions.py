from typing import List, Tuple
from sales_analyzer.core.services.suggestions import ISuggestionsService
from sales_analyzer.web.api.schemas.common import SaleUnit
from sales_analyzer.infrastructure.config import config


DishMargin = Tuple[str, float]
DishQuantity = Tuple[str, int]


class SuggestionService(ISuggestionsService):
    def get_suggestions(
        self,
        margin_dishes_top: List[DishMargin],
        sales_quantity_dishes_top: List[DishQuantity]
    ) -> List[str]:
        """
        Выдача рекоммендаций.
        """
        result_suggestions = list()

        # рекоммендации по бест селлерам
        best_sellers_suggestions = self.recommend_best_sellers(sales_quantity_dishes_top)
        
        # рекоммендации по низкомаржинальным блюдам
        recommend_raise_price_for_low_margin = self.price_raise_recommendations(margin_dishes_top)

        result_suggestions.extend(best_sellers_suggestions)
        result_suggestions.extend(recommend_raise_price_for_low_margin)
        
        return result_suggestions
    
    @staticmethod
    def recommend_best_sellers(sales_quantity_dishes_top: List[DishQuantity]):
        """
        Блюдо много продается, можно добавить в рекоммендации.
        """
        res_suggestions = []
        for dish, quantity in sales_quantity_dishes_top:
            if quantity >= config.ANALYZER_CONFIG.BEST_SELLER_QUANTITY_THRESHOLD:
                res_suggestions.append(f'Блюдо {dish} хорошо продается, можно добавить в рекоммендации.')
        
        return res_suggestions
    
    @staticmethod
    def price_raise_recommendations(margin_dishes_top: List[DishMargin]):
        """
        Блюдо немаржинальное, можно повысить цену.
        """
        res_suggestions = []

        for dish, margin in margin_dishes_top[::-1]:
            if margin < config.ANALYZER_CONFIG.LOSS_MAKING_MARGIN_THRESHOLD:
                res_suggestions.append(f'Увеличить цену на {dish}.')
        
        return res_suggestions
    

def get_suggestions_service() -> ISuggestionsService:
    return SuggestionService()
