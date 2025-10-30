from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email debe ser válido')
        return v.lower()


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    roles: List[str]


class UserProfile(BaseModel):
    usuario_id: int
    email: str
    nombre: str
    apellido: str
    empresa_id: Optional[int] = None
    telefono: Optional[str] = None
    status: str
    last_login: Optional[datetime] = None
    created_at: datetime


class UsuarioCreateDTO(BaseModel):
    empresa_id: Optional[int] = None
    email: str
    password: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email debe ser válido')
        return v.lower()


class UsuarioUpdateDTO(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    status: Optional[str] = None


class UsuarioResponseDTO(BaseModel):
    usuario_id: int
    empresa_id: Optional[int] = None
    email: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    status: str
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RolCreateDTO(BaseModel):
    role_name: str
    description: Optional[str] = None
    permissions: Optional[str] = None


class RolResponseDTO(BaseModel):
    role_id: int
    role_name: str
    description: Optional[str] = None
    permissions: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UsuarioRolCreateDTO(BaseModel):
    usuario_id: int
    role_id: int
    assigned_by: int


class UsuarioRolResponseDTO(BaseModel):
    usuario_role_id: int
    usuario_id: int
    role_id: int
    assigned_by: int
    assigned_at: datetime
    status: str

    class Config:
        from_attributes = True
