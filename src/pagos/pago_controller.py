from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..shared.database import get_db
from .dto.pago_dto import PagoCreateDTO, PagoUpdateDTO, PagoResponseDTO, PagoListDTO, PagoCompletarDTO
from .pago_service import PagoService

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.post("/", response_model=PagoResponseDTO, status_code=201)
async def crear_pago(
    pago_data: PagoCreateDTO,
    db: Session = Depends(get_db)
):
    try:
        service = PagoService(db)
        return service.crear_pago(pago_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pago_id}", response_model=PagoResponseDTO)
async def obtener_pago(
    pago_id: int,
    db: Session = Depends(get_db)
):
    service = PagoService(db)
    pago = service.obtener_pago(pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.get("/transaccion/{transaccion_id}", response_model=List[PagoResponseDTO])
async def listar_pagos_por_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db)
):
    service = PagoService(db)
    return service.listar_pagos_por_transaccion(transaccion_id)


@router.get("/status/{status}", response_model=PagoListDTO)
async def listar_pagos_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = PagoService(db)
    return service.listar_pagos_por_status(status, page=page, size=size)


@router.post("/{pago_id}/completar", response_model=PagoResponseDTO)
async def completar_pago(
    pago_id: int,
    completar_data: PagoCompletarDTO,
    db: Session = Depends(get_db)
):
    service = PagoService(db)
    pago = service.completar_pago(pago_id, completar_data)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.put("/{pago_id}", response_model=PagoResponseDTO)
async def actualizar_pago(
    pago_id: int,
    pago_data: PagoUpdateDTO,
    db: Session = Depends(get_db)
):
    service = PagoService(db)
    pago = service.actualizar_pago(pago_id, pago_data)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.get("/pendientes/listar", response_model=List[PagoResponseDTO])
async def obtener_pagos_pendientes(db: Session = Depends(get_db)):
    service = PagoService(db)
    return service.obtener_pagos_pendientes()


@router.get("/resumen/summary")
async def obtener_resumen_pagos(db: Session = Depends(get_db)):
    service = PagoService(db)
    return service.obtener_resumen_pagos()
