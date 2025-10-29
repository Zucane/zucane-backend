from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..shared.database import get_db
from .dto.token_dto import TokenCreateDTO, TokenUpdateDTO, TokenResponseDTO, TokenListDTO, TokenReservaDTO
from .token_service import TokenService

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("/", response_model=TokenResponseDTO, status_code=201)
async def emitir_token(
    token_data: TokenCreateDTO,
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    return service.emitir_token(token_data)


@router.get("/{token_id}", response_model=TokenResponseDTO)
async def obtener_token(
    token_id: int,
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    token = service.obtener_token(token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    return token


@router.get("/", response_model=TokenListDTO)
async def listar_tokens_disponibles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    return service.listar_tokens_disponibles(page=page, size=size)


@router.get("/status/{status}", response_model=TokenListDTO)
async def listar_tokens_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    return service.listar_tokens_por_status(status, page=page, size=size)


@router.post("/reservar", response_model=List[TokenResponseDTO])
async def reservar_tokens(
    reserva_data: TokenReservaDTO,
    db: Session = Depends(get_db)
):
    try:
        service = TokenService(db)
        return service.reservar_tokens(reserva_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/liberar", response_model=List[TokenResponseDTO])
async def liberar_tokens(
    token_ids: List[int],
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    return service.liberar_tokens(token_ids)


@router.post("/vender", response_model=List[TokenResponseDTO])
async def vender_tokens(
    token_ids: List[int],
    db: Session = Depends(get_db)
):
    service = TokenService(db)
    return service.vender_tokens(token_ids)


@router.get("/inventario/summary")
async def obtener_inventario(db: Session = Depends(get_db)):
    service = TokenService(db)
    return service.obtener_inventario()
