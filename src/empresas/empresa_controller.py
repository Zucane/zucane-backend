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
    ## 🏢 Crear Nueva Empresa
    
    Registra una nueva empresa en el sistema para que pueda comprar tokens de CO2.
    
    ### Parámetros
    - **rfc**: RFC de la empresa (13 caracteres)
    - **nombre**: Nombre de la empresa
    - **email**: Correo electrónico de contacto
    - **telefono**: Teléfono de contacto
    - **direccion**: Dirección física
    
    ### Respuesta
    - **empresa_id**: ID único de la empresa
    - **rfc**: RFC validado
    - **nombre**: Nombre de la empresa
    - **email**: Email de contacto
    - **telefono**: Teléfono
    - **direccion**: Dirección
    - **registro_fecha**: Fecha de registro
    - **status**: Estado actual (activo/inactivo)
    
    ### Errores
    - **400**: RFC duplicado o datos inválidos
    - **422**: Error de validación
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
    service = EmpresaService(db)
    return service.listar_empresas(page=page, size=size, status=status)


@router.put("/{empresa_id}", response_model=EmpresaResponseDTO)
async def actualizar_empresa(
    empresa_id: int,
    empresa_data: EmpresaUpdateDTO,
    db: Session = Depends(get_db)
):
    service = EmpresaService(db)
    empresa = service.actualizar_empresa(empresa_id, empresa_data)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.delete("/{empresa_id}", status_code=204)
async def desactivar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    service = EmpresaService(db)
    if not service.desactivar_empresa(empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
