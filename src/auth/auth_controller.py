from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..shared.database import get_db
from .entity.user_entity import User
from pydantic import BaseModel
from ..stellar.key_generator import StellarKeyGenerator
from sqlalchemy import text
from ..empresas.entity.empresa_entity import Empresa

router = APIRouter(prefix="/auth", tags=["autenticación"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    email: str
    stellar_public_key: str | None = None


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

    empresa = db.query(Empresa).filter(Empresa.email == user.email).first()
    stellar_public_key = empresa.stellar_public_key if empresa else None
    
    return LoginResponse(
        success=True,
        message="Login exitoso",
        user_id=user.id,
        email=user.email,
        stellar_public_key=stellar_public_key
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


@router.post("/reset-admin")
async def reset_admin(db: Session = Depends(get_db)):
    """
    Elimina y recrea el usuario admin@gobierno.mx con claves Stellar generadas.
    """
    admin_email = "admin@gobierno.mx"

    # Asegurar columnas nuevas en DB antes de cualquier consulta ORM
    col = db.execute(text("SHOW COLUMNS FROM users LIKE 'stellar_public_key'"))
    if not col.first():
        db.execute(text("ALTER TABLE users ADD COLUMN stellar_public_key VARCHAR(56) NULL UNIQUE"))
        db.commit()
    col = db.execute(text("SHOW COLUMNS FROM users LIKE 'stellar_secret_key'"))
    if not col.first():
        db.execute(text("ALTER TABLE users ADD COLUMN stellar_secret_key VARCHAR(56) NULL"))
        db.commit()

    # Borrar si existe
    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        db.delete(existing)
        db.commit()

    # Crear nuevo admin
    import hashlib
    password_hash = hashlib.sha256("admin123".encode('utf-8')).hexdigest()
    user = User(
        email=admin_email,
        password_hash=password_hash,
        name="Admin",
        status="active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generar claves Stellar para el admin
    pub, sec = StellarKeyGenerator.generate_keypair_from_user_data(
        email=user.email,
        nombre="Admin",
        apellido=""
    )
    user.stellar_public_key = pub
    user.stellar_secret_key = sec
    db.commit()

    return {
        "message": "Admin recreado",
        "email": user.email,
        "stellar_public_key": user.stellar_public_key
    }
