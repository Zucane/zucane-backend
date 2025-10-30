from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from stellar_sdk import StrKey


class EmpresaCreateDTO(BaseModel):
    rfc: str
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    stellar_public_key: str
    
    @validator('rfc')
    def validate_rfc(cls, v):
        if len(v) != 13:
            raise ValueError('RFC debe tener 13 caracteres')
        return v.upper()
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email debe ser válido')
        return v.lower()
    
    @validator('stellar_public_key')
    def validate_stellar_key(cls, v):
        if not v:
            raise ValueError('Stellar public key es requerido')
        
        # Validar formato básico
        if len(v) != 56:
            raise ValueError('Stellar public key debe tener 56 caracteres')
        if not v.startswith('G'):
            raise ValueError('Stellar public key debe empezar con G')
        
        # Validar que sea una clave Stellar real usando Stellar SDK
        try:
            StrKey.decode_ed25519_public_key(v)
        except Exception:
            raise ValueError('Clave Stellar inválida. Debe ser una clave pública válida de Stellar')
        
        return v


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
    
    class Config:
        from_attributes = True


class EmpresaListDTO(BaseModel):
    empresas: list[EmpresaResponseDTO]
    total: int
    page: int
    size: int
