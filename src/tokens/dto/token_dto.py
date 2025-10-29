from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class TokenCreateDTO(BaseModel):
    cantidad_co2: Decimal
    
    @validator('cantidad_co2')
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad de CO2 debe ser mayor a 0')
        return v


class TokenUpdateDTO(BaseModel):
    cantidad_co2: Optional[Decimal] = None
    status: Optional[str] = None


class TokenResponseDTO(BaseModel):
    token_id: int
    cantidad_co2: Decimal
    fecha_emision: datetime
    status: str
    
    class Config:
        from_attributes = True


class TokenListDTO(BaseModel):
    tokens: List[TokenResponseDTO]
    total: int
    page: int
    size: int


class TokenReservaDTO(BaseModel):
    token_ids: List[int]
    empresa_id: int
