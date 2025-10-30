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
    """
    CREAR AUDITORIA
    
    Crea un nuevo registro de auditoria.
    
    QUE HACE:
    - Registra accion realizada
    - Asocia con entidad afectada
    - Guarda detalles y actor
    
    COMO USAR:
    1. Poner entity_type (tipo de entidad)
    2. Poner entity_id (ID de la entidad)
    3. Poner action (accion realizada)
    4. Poner actor (usuario que actuo)
    5. Opcional: detalles adicionales
    
    RESPUESTA:
    - auditoria_id: ID del registro
    - entity_type: Tipo de entidad
    - entity_id: ID de la entidad
    - action: Accion realizada
    - actor: Usuario que actuo
    - created_at: Fecha de creacion
    """
    service = AuditoriaService(db)
    return service.crear_auditoria(auditoria_data)


@router.get("/{auditoria_id}", response_model=AuditoriaResponseDTO)
async def obtener_auditoria(
    auditoria_id: int,
    db: Session = Depends(get_db)
):
    """
    OBTENER AUDITORIA
    
    Obtiene un registro de auditoria por su ID.
    
    QUE HACE:
    - Busca auditoria por ID
    - Devuelve todos los datos
    - Incluye detalles completos
    
    COMO USAR:
    1. Poner auditoria_id en la URL
    2. Llamar GET
    3. Ver datos completos
    
    RESPUESTA:
    - auditoria_id: ID del registro
    - entity_type: Tipo de entidad
    - entity_id: ID de la entidad
    - action: Accion realizada
    - actor: Usuario que actuo
    - created_at: Fecha de creacion
    """
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
    """
    LISTAR AUDITORIAS POR TRANSACCION
    
    Obtiene auditorias de una transaccion especifica.
    
    QUE HACE:
    - Busca auditorias por transaccion_id
    - Aplica paginacion
    - Devuelve historial completo
    
    COMO USAR:
    1. Poner transaccion_id en la URL
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - auditorias: Lista de auditorias
    - total: Total de auditorias
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = AuditoriaService(db)
    return service.listar_auditorias_por_transaccion(transaccion_id, page=page, size=size)


@router.get("/usuario/{usuario_id}", response_model=AuditoriaListDTO)
async def listar_auditorias_por_usuario(
    usuario_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    LISTAR AUDITORIAS POR USUARIO
    
    Obtiene auditorias de un usuario especifico.
    
    QUE HACE:
    - Busca auditorias por usuario_id
    - Aplica paginacion
    - Devuelve historial del usuario
    
    COMO USAR:
    1. Poner usuario_id en la URL
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - auditorias: Lista de auditorias
    - total: Total de auditorias
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = AuditoriaService(db)
    return service.listar_auditorias_por_usuario(usuario_id, page=page, size=size)


@router.post("/buscar", response_model=AuditoriaListDTO)
async def buscar_auditorias(
    filtros: AuditoriaFiltrosDTO,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    BUSCAR AUDITORIAS
    
    Busca auditorias con filtros especificos.
    
    QUE HACE:
    - Aplica filtros de busqueda
    - Busca por criterios multiples
    - Devuelve resultados filtrados
    
    COMO USAR:
    1. Enviar filtros en el body
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar POST
    
    RESPUESTA:
    - auditorias: Lista de auditorias
    - total: Total de resultados
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = AuditoriaService(db)
    return service.buscar_auditorias(filtros, page=page, size=size)


@router.get("/", response_model=AuditoriaListDTO)
async def listar_todas_auditorias(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    LISTAR TODAS LAS AUDITORIAS
    
    Obtiene todas las auditorias del sistema.
    
    QUE HACE:
    - Lista todas las auditorias
    - Aplica paginacion
    - Devuelve historial completo
    
    COMO USAR:
    1. Opcional: page (pagina, default 1)
    2. Opcional: size (tamano, default 10)
    3. Llamar GET
    
    RESPUESTA:
    - auditorias: Lista de auditorias
    - total: Total de auditorias
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = AuditoriaService(db)
    return service.listar_todas_auditorias(page=page, size=size)


@router.put("/{auditoria_id}", response_model=AuditoriaResponseDTO)
async def actualizar_auditoria(
    auditoria_id: int,
    auditoria_data: AuditoriaUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    ACTUALIZAR AUDITORIA
    
    Actualiza un registro de auditoria existente.
    
    QUE HACE:
    - Actualiza campos enviados
    - Valida datos nuevos
    - Mantiene campos no enviados
    
    COMO USAR:
    1. Poner auditoria_id en la URL
    2. Enviar solo campos a actualizar
    3. Llamar PUT
    
    RESPUESTA:
    - auditoria_id: ID del registro
    - Datos actualizados
    - Campos no enviados sin cambios
    """
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
    """
    REGISTRAR ACCION
    
    Registra una accion de auditoria de forma rapida.
    
    QUE HACE:
    - Crea registro de auditoria
    - Asocia con transaccion
    - Registra accion y detalles
    
    COMO USAR:
    1. Poner transaccion_id en query
    2. Poner accion en query
    3. Opcional: detalles en query
    4. Opcional: usuario_id en query
    5. Llamar POST
    
    RESPUESTA:
    - auditoria_id: ID del registro
    - transaccion_id: ID de la transaccion
    - action: Accion registrada
    - detalles: Detalles registrados
    """
    service = AuditoriaService(db)
    return service.registrar_accion(transaccion_id, accion, detalles, usuario_id)


@router.get("/resumen/summary")
async def obtener_resumen_auditoria(db: Session = Depends(get_db)):
    """
    RESUMEN DE AUDITORIA
    
    Obtiene resumen estadistico de auditorias.
    
    QUE HACE:
    - Cuenta auditorias por tipo
    - Calcula estadisticas
    - Devuelve resumen completo
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Ver resumen completo
    
    RESPUESTA:
    - total_auditorias: Total de auditorias
    - por_entidad: Auditorias por entidad
    - por_accion: Auditorias por accion
    - por_usuario: Auditorias por usuario
    """
    service = AuditoriaService(db)
    return service.obtener_resumen_auditoria()
