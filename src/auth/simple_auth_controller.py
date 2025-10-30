from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..shared.database import get_db
from .dto.auth_dto import LoginRequest, LoginResponse, UserProfile
from .entity.usuario_entity import Usuario

router = APIRouter(prefix="/auth", tags=["autenticación simple"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar contraseña (hash simple)
    import hashlib
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
    if password_hash != user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar que el usuario esté activo
    if user.status != 'activo':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    # Respuesta simple sin JWT
    return LoginResponse(
        access_token="simple_token_12345",
        token_type="simple",
        user_id=user.usuario_id,
        email=user.email,
        roles=["GOV_ADMIN"]
    )


@router.get("/profile")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    # Buscar usuario por ID
    user = db.query(Usuario).filter(Usuario.usuario_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserProfile(
        usuario_id=user.usuario_id,
        email=user.email,
        nombre=user.nombre,
        apellido=user.apellido,
        empresa_id=user.empresa_id,
        telefono=user.telefono,
        status=user.status,
        last_login=user.last_login,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout():
    return {"message": "Logout exitoso"}
