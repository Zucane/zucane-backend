from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from stellar_sdk import StrKey


class TokenCreateDTO(BaseModel):
    cantidad_co2: Decimal
    status: str = "disponible"
    asset_code: str = "XOCHI"
    issuer_pubkey: str
    dist_pubkey: str
    
    @validator('cantidad_co2')
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad de CO2 debe ser mayor a 0')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["disponible", "reservado", "vendido"]
        if v not in valid_statuses:
            raise ValueError(f'Status debe ser uno de: {", ".join(valid_statuses)}')
        return v
    
    @validator('issuer_pubkey')
    def validate_issuer_pubkey(cls, v):
        if not v:
            raise ValueError('Issuer public key es requerido')
        if len(v) != 56:
            raise ValueError('Issuer public key debe tener 56 caracteres')
        if not v.startswith('G'):
            raise ValueError('Issuer public key debe empezar con G')
        try:
            StrKey.decode_ed25519_public_key(v)
        except Exception:
            raise ValueError('Issuer public key inválida')
        return v
    
    @validator('dist_pubkey')
    def validate_dist_pubkey(cls, v):
        if not v:
            raise ValueError('Distribution public key es requerido')
        if len(v) != 56:
            raise ValueError('Distribution public key debe tener 56 caracteres')
        if not v.startswith('G'):
            raise ValueError('Distribution public key debe empezar con G')
        try:
            StrKey.decode_ed25519_public_key(v)
        except Exception:
            raise ValueError('Distribution public key inválida')
        return v


class TokenUpdateDTO(BaseModel):
    cantidad_co2: Optional[Decimal] = None
    status: Optional[str] = None


class TokenResponseDTO(BaseModel):
    token_id: int
    cantidad_co2: Decimal
    fecha_emision: datetime
    status: str
    asset_code: str
    issuer_pubkey: str
    dist_pubkey: str
    
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
