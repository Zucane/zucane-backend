from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class EmpresaCreateDTO(BaseModel):
    rfc: str
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    
    @validator('rfc')
    def validate_rfc(cls, v):
        if len(v) != 13:
            raise ValueError('RFC debe tener 13 caracteres')
        return v.upper()


class EmpresaUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    status: Optional[str] = None


class EmpresaResponseDTO(BaseModel):
    empresa_id: int
    rfc: str
    nombre: str
    email: str
    telefono: Optional[str]
    direccion: Optional[str]
    registro_fecha: datetime
    status: str
    
    class Config:
        from_attributes = True


class EmpresaListDTO(BaseModel):
    empresas: list[EmpresaResponseDTO]
    total: int
    page: int
    size: int
