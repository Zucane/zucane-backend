from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..shared.database import get_db
from .dto.auditoria_dto import (
    AuditoriaCreateDTO, 
    AuditoriaUpdateDTO, 
    AuditoriaResponseDTO, 
    AuditoriaListDTO, 
    AuditoriaFiltrosDTO
)
from .auditoria_service import AuditoriaService

router = APIRouter(prefix="/auditoria", tags=["auditoria"])


@router.post("/", response_model=AuditoriaResponseDTO, status_code=201)
async def crear_auditoria(
    auditoria_data: AuditoriaCreateDTO,
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.crear_auditoria(auditoria_data)


@router.get("/{auditoria_id}", response_model=AuditoriaResponseDTO)
async def obtener_auditoria(
    auditoria_id: int,
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    auditoria = service.obtener_auditoria(auditoria_id)
    if not auditoria:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    return auditoria


@router.get("/transaccion/{transaccion_id}", response_model=AuditoriaListDTO)
async def listar_auditorias_por_transaccion(
    transaccion_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.listar_auditorias_por_transaccion(transaccion_id, page=page, size=size)


@router.get("/usuario/{usuario_id}", response_model=AuditoriaListDTO)
async def listar_auditorias_por_usuario(
    usuario_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.listar_auditorias_por_usuario(usuario_id, page=page, size=size)


@router.post("/buscar", response_model=AuditoriaListDTO)
async def buscar_auditorias(
    filtros: AuditoriaFiltrosDTO,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.buscar_auditorias(filtros, page=page, size=size)


@router.get("/", response_model=AuditoriaListDTO)
async def listar_todas_auditorias(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.listar_todas_auditorias(page=page, size=size)


@router.put("/{auditoria_id}", response_model=AuditoriaResponseDTO)
async def actualizar_auditoria(
    auditoria_id: int,
    auditoria_data: AuditoriaUpdateDTO,
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    auditoria = service.actualizar_auditoria(auditoria_id, auditoria_data)
    if not auditoria:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    return auditoria


@router.post("/registrar", response_model=AuditoriaResponseDTO)
async def registrar_accion(
    transaccion_id: int = Query(...),
    accion: str = Query(...),
    detalles: str = Query(""),
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    service = AuditoriaService(db)
    return service.registrar_accion(transaccion_id, accion, detalles, usuario_id)


@router.get("/resumen/summary")
async def obtener_resumen_auditoria(db: Session = Depends(get_db)):
    service = AuditoriaService(db)
    return service.obtener_resumen_auditoria()
