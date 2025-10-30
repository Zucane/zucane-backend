from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..shared.database import get_db
from .dto.empresa_dto import EmpresaCreateDTO, EmpresaUpdateDTO, EmpresaResponseDTO, EmpresaListDTO
from .empresa_service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["empresas"])


@router.post("/", response_model=EmpresaResponseDTO, status_code=201)
async def crear_empresa(
    empresa_data: EmpresaCreateDTO,
    db: Session = Depends(get_db)
):
    """
    CREAR EMPRESA
    
    Registra una nueva empresa en el sistema.
    
    QUE HACE:
    - Valida RFC (13 caracteres)
    - Valida email
    - Valida clave Stellar publica
    - Crea empresa con status "activo"
    
    COMO USAR:
    1. Poner RFC de 13 caracteres
    2. Poner nombre y email
    3. Poner clave Stellar publica valida
    4. Opcional: telefono y direccion
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - rfc: RFC validado
    - nombre: Nombre de la empresa
    - status: "activo"
    - stellar_public_key: Clave Stellar
    """
    try:
        service = EmpresaService(db)
        return service.crear_empresa(empresa_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{empresa_id}", response_model=EmpresaResponseDTO)
async def obtener_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """
    OBTENER EMPRESA
    
    Obtiene una empresa por su ID.
    
    QUE HACE:
    - Busca empresa por ID
    - Devuelve todos los datos
    - Incluye status y fechas
    
    COMO USAR:
    1. Poner empresa_id en la URL
    2. Llamar GET
    3. Ver datos completos
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - rfc: RFC de la empresa
    - nombre: Nombre de la empresa
    - email: Email de contacto
    - status: Estado actual
    - stellar_public_key: Clave Stellar
    """
    service = EmpresaService(db)
    empresa = service.obtener_empresa(empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.get("/rfc/{rfc}", response_model=EmpresaResponseDTO)
async def obtener_empresa_por_rfc(
    rfc: str,
    db: Session = Depends(get_db)
):
    """
    OBTENER EMPRESA POR RFC
    
    Busca una empresa por su RFC.
    
    QUE HACE:
    - Busca empresa por RFC
    - Devuelve datos completos
    - RFC debe existir en el sistema
    
    COMO USAR:
    1. Poner RFC en la URL
    2. Llamar GET
    3. Ver datos de la empresa
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - rfc: RFC buscado
    - nombre: Nombre de la empresa
    - email: Email de contacto
    - status: Estado actual
    """
    service = EmpresaService(db)
    empresa = service.obtener_empresa_por_rfc(rfc)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.get("/", response_model=EmpresaListDTO)
async def listar_empresas(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: str = Query("activo"),
    db: Session = Depends(get_db)
):
    """
    LISTAR EMPRESAS
    
    Obtiene lista paginada de empresas.
    
    QUE HACE:
    - Lista empresas con paginacion
    - Filtra por status (activo/inactivo)
    - Devuelve total y metadatos
    
    COMO USAR:
    1. Opcional: page (pagina, default 1)
    2. Opcional: size (tamano, default 10)
    3. Opcional: status (activo/inactivo, default activo)
    4. Llamar GET
    
    RESPUESTA:
    - empresas: Lista de empresas
    - total: Total de empresas
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = EmpresaService(db)
    return service.listar_empresas(page=page, size=size, status=status)


@router.put("/{empresa_id}", response_model=EmpresaResponseDTO)
async def actualizar_empresa(
    empresa_id: int,
    empresa_data: EmpresaUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    ACTUALIZAR EMPRESA
    
    Actualiza datos de una empresa existente.
    
    QUE HACE:
    - Actualiza campos enviados
    - Valida datos nuevos
    - Mantiene campos no enviados
    
    COMO USAR:
    1. Poner empresa_id en la URL
    2. Enviar solo campos a actualizar
    3. Llamar PUT
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - Datos actualizados
    - Campos no enviados sin cambios
    """
    service = EmpresaService(db)
    empresa = service.actualizar_empresa(empresa_id, empresa_data)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.patch("/{empresa_id}/desactivar", response_model=EmpresaResponseDTO)
async def desactivar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """
    DESACTIVAR EMPRESA
    
    Desactiva una empresa (cambia status a inactivo).
    
    QUE HACE:
    - Cambia status a "inactivo"
    - Empresa no puede hacer transacciones
    - Mantiene datos historicos
    
    COMO USAR:
    1. Poner empresa_id en la URL
    2. Llamar PATCH
    3. Empresa queda inactiva
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - status: "inactivo"
    - Datos sin cambios
    """
    service = EmpresaService(db)
    empresa = service.desactivar_empresa(empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.patch("/{empresa_id}/activar", response_model=EmpresaResponseDTO)
async def activar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """
    ACTIVAR EMPRESA
    
    Activa una empresa (cambia status a activo).
    
    QUE HACE:
    - Cambia status a "activo"
    - Empresa puede hacer transacciones
    - Restaura funcionalidad completa
    
    COMO USAR:
    1. Poner empresa_id en la URL
    2. Llamar PATCH
    3. Empresa queda activa
    
    RESPUESTA:
    - empresa_id: ID de la empresa
    - status: "activo"
    - Datos sin cambios
    """
    service = EmpresaService(db)
    empresa = service.activar_empresa(empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa
