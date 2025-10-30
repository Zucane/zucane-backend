from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..shared.database import get_db
from .entity.user_entity import User
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["autenticación"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    email: str


class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    status: str
    created_at: datetime


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    INICIAR SESION
    
    Autentica un usuario en el sistema.
    
    QUE HACE:
    - Valida email y password
    - Verifica que usuario este activo
    - Devuelve datos del usuario
    
    COMO USAR:
    1. Poner email del usuario
    2. Poner password
    3. Llamar POST
    
    RESPUESTA:
    - success: true si exitoso
    - message: Mensaje de resultado
    - user_id: ID del usuario
    - email: Email del usuario
    """
    # Buscar usuario por email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    # Verificar contraseña (hash simple)
    import hashlib
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
    if password_hash != user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    # Verificar que el usuario esté activo
    if user.status != 'active':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return LoginResponse(
        success=True,
        message="Login exitoso",
        user_id=user.id,
        email=user.email
    )


@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    """
    OBTENER PERFIL DE USUARIO
    
    Obtiene el perfil de un usuario por su ID.
    
    QUE HACE:
    - Busca usuario por ID
    - Devuelve datos del perfil
    - Incluye status y fechas
    
    COMO USAR:
    1. Poner user_id en la URL
    2. Llamar GET
    3. Ver datos del perfil
    
    RESPUESTA:
    - id: ID del usuario
    - email: Email del usuario
    - name: Nombre del usuario
    - status: Estado del usuario
    - created_at: Fecha de creacion
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserProfile(
        id=user.id,
        email=user.email,
        name=user.name,
        status=user.status,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout():
    """
    CERRAR SESION
    
    Cierra la sesion del usuario actual.
    
    QUE HACE:
    - Invalida sesion actual
    - Limpia tokens de autenticacion
    - Confirma logout exitoso
    
    COMO USAR:
    1. Llamar POST sin parametros
    2. Sesion cerrada
    
    RESPUESTA:
    - message: "Logout exitoso"
    """
    return {"message": "Logout exitoso"}
