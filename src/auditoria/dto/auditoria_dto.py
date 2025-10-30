from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class AuditoriaCreateDTO(BaseModel):
    transaccion_id: int
    usuario_id: Optional[int] = None
    accion: str
    detalles: str = ""
    
    @validator('accion')
    def validate_accion(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('La acción no puede estar vacía')
        return v.strip()


class AuditoriaUpdateDTO(BaseModel):
    detalles: Optional[str] = None


class AuditoriaResponseDTO(BaseModel):
    audit_id: int
    entity_type: str
    entity_id: int
    actor: str
    action: str
    fecha_accion: datetime
    detalles: str
    idempotency_key: Optional[str] = None
    stellar_tx_hash: Optional[str] = None
    auditoria_id: Optional[int] = None
    transaccion_id: Optional[int] = None
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    
    class Config:
        from_attributes = True


class AuditoriaListDTO(BaseModel):
    auditorias: list[AuditoriaResponseDTO]
    total: int
    page: int
    size: int


class AuditoriaFiltrosDTO(BaseModel):
    transaccion_id: Optional[int] = None
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
