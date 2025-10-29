from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..shared.database import get_db
from ..shared.auth import auth_service, get_current_user
from .dto.auth_dto import LoginRequest, LoginResponse, UserProfile
from .entity.usuario_entity import Usuario

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):

    return LoginResponse(
        access_token="placeholder_token",
        token_type="bearer",
        user_id=1,
        email=login_data.email,
        roles=["COMPANY_USER"]
    )


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: Usuario = Depends(get_current_user)):
    return UserProfile(
        usuario_id=current_user.usuario_id,
        email=current_user.email,
        nombre=current_user.nombre,
        apellido=current_user.apellido,
        empresa_id=current_user.empresa_id,
        telefono=current_user.telefono,
        status=current_user.status,
        last_login=current_user.last_login,
        created_at=current_user.created_at
    )


@router.post("/logout")
async def logout():

    return {"message": "Logout exitoso"}
