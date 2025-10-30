from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

from ..auth.entity.usuario_entity import Usuario
from ..auth.entity.rol_entity import Rol
from ..auth.entity.usuario_rol_entity import UsuarioRol

security = HTTPBearer()


class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    
    def get_user_roles(self, db: Session, usuario_id: int) -> List[str]:
        # Simplificado temporalmente - devolver rol por defecto
        return ["GOV_ADMIN"]


auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    usuario_id = payload.get("sub")
    
    # Convertir a int si es necesario
    if isinstance(usuario_id, str):
        usuario_id = int(usuario_id)
    
    user = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return user


def require_roles(required_roles: List[str]):
    def role_checker(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
        user_roles = auth_service.get_user_roles(db, current_user.usuario_id)
        
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes"
            )
        
        return current_user
    
    return role_checker

require_gov_admin = require_roles(['GOV_ADMIN'])
require_company_user = require_roles(['COMPANY_USER'])
require_any_user = require_roles(['GOV_ADMIN', 'COMPANY_USER'])
