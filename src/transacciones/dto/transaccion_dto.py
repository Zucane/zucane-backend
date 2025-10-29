from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class TransaccionCreateDTO(BaseModel):
    empresa_id: int
    token_id: int
    monto: Decimal
    
    @validator('monto')
    def validate_monto(cls, v):
        if v <= 0:
            raise ValueError('El monto debe ser mayor a 0')
        return v


class TransaccionUpdateDTO(BaseModel):
    status: Optional[str] = None
    stellar_tx_hash: Optional[str] = None
    stellar_asset_code: Optional[str] = None


class TransaccionResponseDTO(BaseModel):
    transaccion_id: int
    empresa_id: int
    token_id: int
    monto: Decimal
    fecha_compra: datetime
    status: str
    stellar_tx_hash: Optional[str]
    stellar_asset_code: Optional[str]
    
    class Config:
        from_attributes = True


class TransaccionListDTO(BaseModel):
    transacciones: List[TransaccionResponseDTO]
    total: int
    page: int
    size: int


class TransaccionConfirmarDTO(BaseModel):
    stellar_tx_hash: str
    stellar_asset_code: str
