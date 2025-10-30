from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class EmpresaCreateDTO(BaseModel):
    rfc: str
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    # stellar_public_key se genera automáticamente
    
    @validator('rfc')
    def validate_rfc(cls, v):
        # Validación básica: solo verificar que no esté vacío
        if not v or len(v.strip()) == 0:
            raise ValueError('RFC es requerido')
        return v.upper().strip()
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email debe ser válido')
        return v.lower()


class EmpresaUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    status: Optional[str] = None
    stellar_public_key: Optional[str] = None


class EmpresaResponseDTO(BaseModel):
    empresa_id: int
    rfc: str
    nombre: str
    email: str
    telefono: Optional[str]
    direccion: Optional[str]
    registro_fecha: datetime
    status: str
    stellar_public_key: str
    stellar_secret_key: Optional[str] = None  # Solo para mostrar en creación
    
    class Config:
        from_attributes = True


class EmpresaListDTO(BaseModel):
    empresas: list[EmpresaResponseDTO]
    total: int
    page: int
    size: int
