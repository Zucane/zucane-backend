from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from ..shared.database import get_db
from .dto.transaccion_dto import TransaccionCreateDTO, TransaccionUpdateDTO, TransaccionResponseDTO, TransaccionListDTO, TransaccionConfirmarDTO
from ..payments.dto.payment_dto import PaymentRequestDTO, PaymentResponseDTO, PaymentVerificationDTO, PaymentVerificationResponseDTO, BalanceRequestDTO, BalanceResponseDTO
from .transaccion_service import TransaccionService

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.post("/", response_model=TransaccionResponseDTO, status_code=201)
async def crear_transaccion(
    transaccion_data: TransaccionCreateDTO,
    db: Session = Depends(get_db)
):
    """
    CREAR TRANSACCION
    
    Crea una nueva transacción de compra de tokens.
    
    QUE HACE:
    - Valida que empresa este activa
    - Valida que token este disponible
    - Crea transaccion con status "pendiente"
    - Reserva el token automaticamente
    
    COMO USAR:
    1. Poner empresa_id (debe existir)
    2. Poner token_id (debe estar disponible)
    3. Poner monto a pagar
    4. Llamar endpoint
    
    RESPUESTA:
    - transaccion_id: ID de la transaccion
    - status: "pendiente"
    - monto: Monto de la transaccion
    - fecha_compra: Fecha de creacion
    """
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
    """
    OBTENER TRANSACCION
    
    Obtiene una transaccion por su ID.
    
    QUE HACE:
    - Busca transaccion por ID
    - Devuelve todos los datos
    - Incluye status y fechas
    
    COMO USAR:
    1. Poner transaccion_id en la URL
    2. Llamar GET
    3. Ver datos completos
    
    RESPUESTA:
    - transaccion_id: ID de la transaccion
    - empresa_id: ID de la empresa
    - token_id: ID del token
    - monto: Monto de la transaccion
    - status: Estado actual
    - fecha_compra: Fecha de creacion
    """
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
    """
    LISTAR TRANSACCIONES DE EMPRESA
    
    Obtiene todas las transacciones de una empresa.
    
    QUE HACE:
    - Busca transacciones por empresa_id
    - Aplica paginacion
    - Devuelve lista paginada
    
    COMO USAR:
    1. Poner empresa_id en la URL
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - transacciones: Lista de transacciones
    - total: Total de transacciones
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = TransaccionService(db)
    return service.listar_transacciones_empresa(empresa_id, page=page, size=size)


@router.get("/status/{status}", response_model=TransaccionListDTO)
async def listar_transacciones_por_status(
    status: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    LISTAR TRANSACCIONES POR STATUS
    
    Obtiene transacciones filtradas por status.
    
    QUE HACE:
    - Busca transacciones por status
    - Aplica paginacion
    - Devuelve lista filtrada
    
    COMO USAR:
    1. Poner status en la URL (pendiente, confirmada, fallida)
    2. Opcional: page (pagina, default 1)
    3. Opcional: size (tamano, default 10)
    4. Llamar GET
    
    RESPUESTA:
    - transacciones: Lista de transacciones
    - total: Total de transacciones
    - page: Pagina actual
    - size: Tamano de pagina
    """
    service = TransaccionService(db)
    return service.listar_transacciones_por_status(status, page=page, size=size)


@router.post("/{transaccion_id}/confirmar", response_model=TransaccionResponseDTO)
async def confirmar_transaccion(
    transaccion_id: int,
    confirmar_data: TransaccionConfirmarDTO,
    db: Session = Depends(get_db)
):
    """
    CONFIRMAR TRANSACCION
    
    Confirma una transaccion pendiente con datos de Stellar.
    
    QUE HACE:
    - Actualiza status a "confirmada"
    - Guarda stellar_tx_hash
    - Guarda stellar_asset_code
    - Marca token como vendido
    
    COMO USAR:
    1. Poner transaccion_id en la URL
    2. Enviar stellar_tx_hash y stellar_asset_code
    3. Llamar POST
    
    RESPUESTA:
    - transaccion_id: ID de la transaccion
    - status: "confirmada"
    - stellar_tx_hash: Hash de Stellar
    - stellar_asset_code: Codigo del asset
    """
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
    """
    FALLAR TRANSACCION
    
    Marca una transaccion como fallida y libera el token.
    
    QUE HACE:
    - Actualiza status a "fallida"
    - Libera el token reservado
    - Token vuelve a "disponible"
    
    COMO USAR:
    1. Poner transaccion_id en la URL
    2. Llamar POST
    3. Token se libera automaticamente
    
    RESPUESTA:
    - transaccion_id: ID de la transaccion
    - status: "fallida"
    - token liberado automaticamente
    """
    service = TransaccionService(db)
    transaccion = service.fallar_transaccion(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.get("/pendientes/procesar", response_model=List[TransaccionResponseDTO])
async def procesar_transacciones_pendientes(db: Session = Depends(get_db)):
    """
    PROCESAR TRANSACCIONES PENDIENTES
    
    Obtiene todas las transacciones pendientes para procesamiento.
    
    QUE HACE:
    - Busca transacciones con status "pendiente"
    - Devuelve lista para procesamiento
    - Para uso interno del sistema
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Obtener lista de pendientes
    3. Procesar con Stellar
    
    RESPUESTA:
    - Lista de transacciones pendientes
    - Para procesamiento automatico
    """
    service = TransaccionService(db)
    return service.procesar_transacciones_pendientes()


# ===== ENDPOINTS STELLAR =====

@router.post("/stellar/pagar", response_model=PaymentResponseDTO)
async def procesar_pago_stellar(
    payment_request: PaymentRequestDTO,
    db: Session = Depends(get_db)
):
    """
    PAGAR CON STELLAR
    
    Procesa pago real en la red Stellar.
    
    QUE HACE:
    - Toma una transaccion pendiente
    - Crea pago real en Stellar Network
    - Actualiza status a "confirmada"
    - Marca token como "vendido"
    
    COMO USAR:
    1. Crear transaccion primero
    2. Llamar este endpoint con transaccion_id
    3. Opcional: incluir empresa_secret_key para pago real
    
    RESPUESTA:
    - success: true/false
    - transaction_hash: Hash de Stellar
    - ledger: Numero de ledger
    """
    try:
        service = TransaccionService(db)
        result = service.procesar_pago_stellar(
            transaccion_id=payment_request.transaccion_id,
            empresa_secret_key=payment_request.empresa_secret_key
        )
        return PaymentResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar pago Stellar: {str(e)}"
        )

@router.post("/stellar/verificar", response_model=PaymentVerificationResponseDTO)
async def verificar_pago_stellar(
    verification_request: PaymentVerificationDTO,
    db: Session = Depends(get_db)
):
    """
    VERIFICAR PAGO STELLAR
    
    Verifica si un pago en Stellar fue exitoso.
    
    QUE HACE:
    - Busca transaccion por hash en Stellar
    - Verifica que fue exitosa
    - Devuelve detalles de la transaccion
    
    COMO USAR:
    1. Obtener transaction_hash del pago
    2. Llamar este endpoint
    3. Verificar que verified = true
    
    RESPUESTA:
    - success: true/false
    - verified: true si el pago fue exitoso
    - hash: Hash de la transaccion
    - ledger: Numero de ledger
    """
    try:
        service = TransaccionService(db)
        result = service.verificar_pago_stellar(verification_request.transaction_hash)
        return PaymentVerificationResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar pago Stellar: {str(e)}"
        )

@router.post("/stellar/balance", response_model=BalanceResponseDTO)
async def obtener_balance_empresa_stellar(
    balance_request: BalanceRequestDTO,
    db: Session = Depends(get_db)
):
    """
    CONSULTAR BALANCE STELLAR
    
    Obtiene el balance de una empresa en Stellar.
    
    QUE HACE:
    - Busca la empresa por ID
    - Consulta balance del asset en Stellar
    - Consulta balance XLM en Stellar
    - Verifica que la cuenta existe
    
    COMO USAR:
    1. Poner empresa_id de la empresa
    2. Llamar este endpoint
    3. Ver balances en la respuesta
    
    RESPUESTA:
    - success: true/false
    - xochi_balance: Balance de tokens del asset
    - xlm_balance: Balance de XLM
    - account_exists: true si la cuenta existe
    """
    try:
        service = TransaccionService(db)
        result = service.obtener_balance_empresa(balance_request.empresa_id)
        return BalanceResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener balance Stellar: {str(e)}"
        )
