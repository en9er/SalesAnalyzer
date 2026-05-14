from pydantic import BaseModel, Field


class SaleUnit(BaseModel):
    dish: str = Field(description='Название блюда')
    cost_price: float = Field(description='Себестоимость')
    selling_price: float = Field(description='Цена продажи')
    quantity: int = Field(description='Количество')

