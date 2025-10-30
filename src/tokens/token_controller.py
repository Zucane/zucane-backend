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
    """
    EMITIR TOKEN
    
    Crea un nuevo token de CO2 en el sistema.
    
    QUE HACE:
    - Valida claves Stellar publicas
    - Crea token con status "disponible"
    - Asigna cantidad de CO2
    
    COMO USAR:
    1. Poner cantidad_co2 (decimal)
    2. Poner issuer_pubkey (clave Stellar valida)
    3. Poner dist_pubkey (clave Stellar valida)
    4. Opcional: asset_code (default XOCHI)
    
    RESPUESTA:
    - token_id: ID del token
    - cantidad_co2: Cantidad de CO2
    - status: "disponible"
    - asset_code: Codigo del asset
    - issuer_pubkey: Clave del emisor
    """
    service = TokenService(db)
    return service.emitir_token(token_data)


@router.get("/{token_id}", response_model=TokenResponseDTO)
async def obtener_token(
    token_id: int,
    db: Session = Depends(get_db)
):
    """
    OBTENER TOKEN
    
    Obtiene un token por su ID.
    
    QUE HACE:
    - Busca token por ID
    - Devuelve todos los datos
    - Incluye status y fechas
    
    COMO USAR:
    1. Poner token_id en la URL
    2. Llamar GET
    3. Ver datos completos
    
    RESPUESTA:
    - token_id: ID del token
    - cantidad_co2: Cantidad de CO2
    - status: Estado actual
    - fecha_emision: Fecha de creacion
    - asset_code: Codigo del asset
    """
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
    """
    LISTAR TOKENS DISPONIBLES
    
    Obtiene lista de tokens disponibles para compra.
    
    QUE HACE:
    - Lista tokens con status "disponible"
    - Aplica paginacion
    - Devuelve total y metadatos
    
    COMO USAR:
    1. Opcional: page (pagina, default 1)
    2. Opcional: size (tamano, default 10)
    3. Llamar GET
    
    RESPUESTA:
    - tokens: Lista de tokens disponibles
    - total: Total de tokens
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = TokenService(db)
    return service.listar_tokens_disponibles(page=page, size=size)


@router.get("/status/{status}", response_model=TokenListDTO)
async def listar_tokens_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    LISTAR TOKENS POR STATUS
    
    Obtiene tokens filtrados por status.
    
    QUE HACE:
    - Busca tokens por status
    - Aplica paginacion
    - Devuelve lista filtrada
    
    COMO USAR:
    1. Poner status en la URL (disponible, reservado, vendido)
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - tokens: Lista de tokens
    - total: Total de tokens
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = TokenService(db)
    return service.listar_tokens_por_status(status, page=page, size=size)


@router.post("/reservar", response_model=List[TokenResponseDTO])
async def reservar_tokens(
    reserva_data: TokenReservaDTO,
    db: Session = Depends(get_db)
):
    """
    RESERVAR TOKENS
    
    Reserva tokens para una transaccion pendiente.
    
    QUE HACE:
    - Cambia status a "reservado"
    - Asocia tokens con empresa
    - Evita doble venta
    
    COMO USAR:
    1. Poner token_ids (lista de IDs)
    2. Poner empresa_id
    3. Llamar POST
    
    RESPUESTA:
    - Lista de tokens reservados
    - Status cambiado a "reservado"
    - Asociados con empresa
    """
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
    """
    LIBERAR TOKENS
    
    Libera tokens reservados (vuelven a disponibles).
    
    QUE HACE:
    - Cambia status a "disponible"
    - Desasocia de empresa
    - Permite nueva reserva
    
    COMO USAR:
    1. Poner token_ids (lista de IDs)
    2. Llamar POST
    3. Tokens vuelven disponibles
    
    RESPUESTA:
    - Lista de tokens liberados
    - Status cambiado a "disponible"
    - Listos para nueva reserva
    """
    service = TokenService(db)
    return service.liberar_tokens(token_ids)


@router.post("/vender", response_model=List[TokenResponseDTO])
async def vender_tokens(
    token_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    VENDER TOKENS
    
    Marca tokens como vendidos (transaccion completada).
    
    QUE HACE:
    - Cambia status a "vendido"
    - Confirma venta final
    - Tokens no disponibles
    
    COMO USAR:
    1. Poner token_ids (lista de IDs)
    2. Llamar POST
    3. Tokens marcados como vendidos
    
    RESPUESTA:
    - Lista de tokens vendidos
    - Status cambiado a "vendido"
    - Transaccion completada
    """
    service = TokenService(db)
    return service.vender_tokens(token_ids)


@router.get("/inventario/summary")
async def obtener_inventario(db: Session = Depends(get_db)):
    """
    RESUMEN DE INVENTARIO
    
    Obtiene resumen del inventario de tokens.
    
    QUE HACE:
    - Cuenta tokens por status
    - Calcula totales
    - Devuelve estadisticas
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Ver resumen completo
    
    RESPUESTA:
    - total_tokens: Total de tokens
    - disponibles: Tokens disponibles
    - reservados: Tokens reservados
    - vendidos: Tokens vendidos
    """
    service = TokenService(db)
    return service.obtener_inventario()
