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
    """
    CREAR PAGO
    
    Crea un nuevo pago a productor.
    
    QUE HACE:
    - Crea pago con status "pendiente"
    - Asocia con transaccion
    - Registra monto y datos
    
    COMO USAR:
    1. Poner transaccion_id
    2. Poner monto del pago
    3. Opcional: comprobante_pago y notas
    4. Llamar POST
    
    RESPUESTA:
    - pago_id: ID del pago
    - transaccion_id: ID de la transaccion
    - monto: Monto del pago
    - status: "pendiente"
    - fecha_pago: Fecha de creacion
    """
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
    """
    OBTENER PAGO
    
    Obtiene un pago por su ID.
    
    QUE HACE:
    - Busca pago por ID
    - Devuelve todos los datos
    - Incluye status y fechas
    
    COMO USAR:
    1. Poner pago_id en la URL
    2. Llamar GET
    3. Ver datos completos
    
    RESPUESTA:
    - pago_id: ID del pago
    - transaccion_id: ID de la transaccion
    - monto: Monto del pago
    - status: Estado actual
    - fecha_pago: Fecha de creacion
    """
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
    """
    LISTAR PAGOS POR TRANSACCION
    
    Obtiene todos los pagos de una transaccion.
    
    QUE HACE:
    - Busca pagos por transaccion_id
    - Devuelve lista de pagos
    - Incluye todos los datos
    
    COMO USAR:
    1. Poner transaccion_id en la URL
    2. Llamar GET
    3. Ver lista de pagos
    
    RESPUESTA:
    - Lista de pagos de la transaccion
    - Datos completos de cada pago
    """
    service = PagoService(db)
    return service.listar_pagos_por_transaccion(transaccion_id)


@router.get("/status/{status}", response_model=PagoListDTO)
async def listar_pagos_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    LISTAR PAGOS POR STATUS
    
    Obtiene pagos filtrados por status.
    
    QUE HACE:
    - Busca pagos por status
    - Aplica paginacion
    - Devuelve lista filtrada
    
    COMO USAR:
    1. Poner status en la URL (pendiente, completado, fallido)
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - pagos: Lista de pagos
    - total: Total de pagos
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = PagoService(db)
    return service.listar_pagos_por_status(status, page=page, size=size)


@router.post("/{pago_id}/completar", response_model=PagoResponseDTO)
async def completar_pago(
    pago_id: int,
    completar_data: PagoCompletarDTO,
    db: Session = Depends(get_db)
):
    """
    COMPLETAR PAGO
    
    Marca un pago como completado.
    
    QUE HACE:
    - Cambia status a "completado"
    - Registra comprobante de pago
    - Confirma pago al productor
    
    COMO USAR:
    1. Poner pago_id en la URL
    2. Enviar comprobante_pago
    3. Opcional: notas adicionales
    4. Llamar POST
    
    RESPUESTA:
    - pago_id: ID del pago
    - status: "completado"
    - comprobante_pago: Comprobante registrado
    - fecha_completado: Fecha de completado
    """
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
    """
    ACTUALIZAR PAGO
    
    Actualiza datos de un pago existente.
    
    QUE HACE:
    - Actualiza campos enviados
    - Valida datos nuevos
    - Mantiene campos no enviados
    
    COMO USAR:
    1. Poner pago_id en la URL
    2. Enviar solo campos a actualizar
    3. Llamar PUT
    
    RESPUESTA:
    - pago_id: ID del pago
    - Datos actualizados
    - Campos no enviados sin cambios
    """
    service = PagoService(db)
    pago = service.actualizar_pago(pago_id, pago_data)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.get("/pendientes/listar", response_model=List[PagoResponseDTO])
async def obtener_pagos_pendientes(db: Session = Depends(get_db)):
    """
    LISTAR PAGOS PENDIENTES
    
    Obtiene todos los pagos pendientes.
    
    QUE HACE:
    - Busca pagos con status "pendiente"
    - Devuelve lista completa
    - Para procesamiento manual
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Ver lista de pendientes
    
    RESPUESTA:
    - Lista de pagos pendientes
    - Datos completos de cada pago
    - Para procesamiento manual
    """
    service = PagoService(db)
    return service.obtener_pagos_pendientes()


@router.get("/resumen/summary")
async def obtener_resumen_pagos(db: Session = Depends(get_db)):
    """
    RESUMEN DE PAGOS
    
    Obtiene resumen estadistico de pagos.
    
    QUE HACE:
    - Cuenta pagos por status
    - Calcula totales y montos
    - Devuelve estadisticas
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Ver resumen completo
    
    RESPUESTA:
    - total_pagos: Total de pagos
    - pendientes: Pagos pendientes
    - completados: Pagos completados
    - monto_total: Monto total
    """
    service = PagoService(db)
    return service.obtener_resumen_pagos()
