from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..shared.database import get_db
from .dto.transaccion_dto import TransaccionCreateDTO, TransaccionUpdateDTO, TransaccionResponseDTO, TransaccionListDTO, TransaccionConfirmarDTO
from .transaccion_service import TransaccionService

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.post("/", response_model=TransaccionResponseDTO, status_code=201)
async def crear_transaccion(
    transaccion_data: TransaccionCreateDTO,
    db: Session = Depends(get_db)
):
    try:
        service = TransaccionService(db)
        return service.crear_transaccion(transaccion_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{transaccion_id}", response_model=TransaccionResponseDTO)
async def obtener_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db)
):
    service = TransaccionService(db)
    transaccion = service.obtener_transaccion(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.get("/empresa/{empresa_id}", response_model=TransaccionListDTO)
async def listar_transacciones_empresa(
    empresa_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TransaccionService(db)
    return service.listar_transacciones_empresa(empresa_id, page=page, size=size)


@router.get("/status/{status}", response_model=TransaccionListDTO)
async def listar_transacciones_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TransaccionService(db)
    return service.listar_transacciones_por_status(status, page=page, size=size)


@router.post("/{transaccion_id}/confirmar", response_model=TransaccionResponseDTO)
async def confirmar_transaccion(
    transaccion_id: int,
    confirmar_data: TransaccionConfirmarDTO,
    db: Session = Depends(get_db)
):
    service = TransaccionService(db)
    transaccion = service.confirmar_transaccion(transaccion_id, confirmar_data)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.post("/{transaccion_id}/fallar", response_model=TransaccionResponseDTO)
async def fallar_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db)
):
    service = TransaccionService(db)
    transaccion = service.fallar_transaccion(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.get("/pendientes/procesar", response_model=List[TransaccionResponseDTO])
async def procesar_transacciones_pendientes(db: Session = Depends(get_db)):
    """Procesar transacciones pendientes"""
    service = TransaccionService(db)
    return service.procesar_transacciones_pendientes()
