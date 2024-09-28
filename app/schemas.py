from typing import List
from pydantic import BaseModel, field_validator

class ProductBase(BaseModel):
    name: str
    descr: str
    price: float
    total_amount: int

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    amount: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    status: str
    items: List[OrderItemBase]

    @field_validator('status')
    @classmethod
    def check_status(cls, value):
        if value not in ["В процессе", "Отправлен", "Доставлен"]:
            raise ValueError("Поле статуса должно иметь значение 'В процессе', 'Отправлен' или 'Доставлен'")
        return value
    
    class Config:
        from_attributes = True

class PatchOrderBase(BaseModel):
    status: str
    @field_validator('status')
    @classmethod
    def check_status(cls, value):
        if value not in ["В процессе", "Отправлен", "Доставлен"]:
            raise ValueError("Поле статуса должно иметь значение 'В процессе', 'Отправлен' или 'Доставлен'")
        return value
