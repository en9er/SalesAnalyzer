from typing import List, Tuple


def calculate_revenue(sales_info: List[Tuple[float, int]]) -> float:
    """
    Подсчет общего дохода.

    :param Tuple[Tuple[float, int]] sales_info: Массив[Цена продажи, количество] 
    """
    return sum((price * quantity for price, quantity in sales_info))


def calculate_cost(cost_info: List[Tuple[float, int]]) -> float:
    """
    Подсчет общей себестоимости товаров.

    :param Tuple[Tuple[float, int]] sales_info: Массив[Себестоимость, количество] 
    """
    return sum((cost * quantity for cost, quantity in cost_info))


def calculate_margin(cost_price: float, selling_price: float) -> float:
    """
    Расчет маржинальности.
    """
    return (selling_price - cost_price) / selling_price * 100 
