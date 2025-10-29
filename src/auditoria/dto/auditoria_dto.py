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
    auditoria_id: int
    transaccion_id: int
    usuario_id: Optional[int]
    accion: str
    fecha_accion: datetime
    detalles: str
    
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
