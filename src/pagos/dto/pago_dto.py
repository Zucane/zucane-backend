from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PagoCreateDTO(BaseModel):
    transaccion_id: int
    monto: Decimal
    productor_nombre: str
    productor_rfc: Optional[str] = None
    productor_banco: Optional[str] = None
    productor_cuenta: Optional[str] = None
    
    @validator('monto')
    def validate_monto(cls, v):
        if v <= 0:
            raise ValueError('El monto debe ser mayor a 0')
        return v


class PagoUpdateDTO(BaseModel):
    status: Optional[str] = None
    productor_banco: Optional[str] = None
    productor_cuenta: Optional[str] = None


class PagoResponseDTO(BaseModel):
    pago_id: int
    monto: Decimal
    fecha_pago: datetime
    transaccion_id: int
    status: str
    productor_nombre: str
    productor_rfc: Optional[str]
    productor_banco: Optional[str]
    productor_cuenta: Optional[str]
    
    class Config:
        from_attributes = True


class PagoListDTO(BaseModel):
    pagos: List[PagoResponseDTO]
    total: int
    page: int
    size: int


class PagoCompletarDTO(BaseModel):
    productor_banco: str
    productor_cuenta: str
