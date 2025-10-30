from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderCreateDTO(BaseModel):
    empresa_id: int
    token_ids: List[int]
    expires_minutes: int = 10


class OrderItemResponseDTO(BaseModel):
    order_item_id: int
    order_id: int
    token_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderResponseDTO(BaseModel):
    order_id: int
    empresa_id: int
    status: str
    expires_at: datetime
    created_at: datetime
    order_items: List[OrderItemResponseDTO] = []

    class Config:
        from_attributes = True


class OrderListDTO(BaseModel):
    orders: List[OrderResponseDTO]
    total: int
    page: int
    size: int


class OrderUpdateDTO(BaseModel):
    status: Optional[str] = None


class OrderExpireDTO(BaseModel):
    order_id: int
    reason: str = "expired"
