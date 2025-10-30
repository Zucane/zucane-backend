#!/usr/bin/env python3
"""
Controlador para pagos con Stellar
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..shared.database import get_db
from .payment_service import PaymentService
from .dto.payment_dto import (
    PaymentRequestDTO, 
    PaymentResponseDTO,
    PaymentVerificationDTO,
    PaymentVerificationResponseDTO,
    BalanceRequestDTO,
    BalanceResponseDTO
)

router = APIRouter(prefix="/payments", tags=["pagos-stellar"])

@router.post("/process", response_model=PaymentResponseDTO)
async def procesar_pago(
    payment_request: PaymentRequestDTO,
    db: Session = Depends(get_db)
):
    """
    PROCESAR PAGO STELLAR
    
    Procesa pago directo en Stellar Network.
    
    QUE HACE:
    - Toma transaccion_id
    - Crea pago real en Stellar
    - Actualiza transaccion
    - Marca token como vendido
    
    COMO USAR:
    1. Crear transaccion primero
    2. Llamar con transaccion_id
    3. Opcional: empresa_secret_key
    
    RESPUESTA:
    - success: true/false
    - transaction_hash: Hash de Stellar
    - amount: Monto procesado
    """
    try:
        service = PaymentService(db)
        result = service.process_payment(
            transaccion_id=payment_request.transaccion_id,
            empresa_secret_key=payment_request.empresa_secret_key
        )
        return PaymentResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar pago: {str(e)}"
        )

@router.post("/verify", response_model=PaymentVerificationResponseDTO)
async def verificar_pago(
    verification_request: PaymentVerificationDTO,
    db: Session = Depends(get_db)
):
    """
    VERIFICAR PAGO STELLAR
    
    Verifica si un pago en Stellar fue exitoso.
    
    QUE HACE:
    - Busca transaccion por hash
    - Verifica que fue exitosa
    - Devuelve detalles completos
    
    COMO USAR:
    1. Obtener transaction_hash
    2. Llamar este endpoint
    3. Verificar verified = true
    
    RESPUESTA:
    - success: true/false
    - verified: true si exitoso
    - hash: Hash de transaccion
    - operations: Detalles de operaciones
    """
    try:
        service = PaymentService(db)
        result = service.verify_payment(verification_request.transaction_hash)
        return PaymentVerificationResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar pago: {str(e)}"
        )

@router.post("/balance", response_model=BalanceResponseDTO)
async def obtener_balance_empresa(
    balance_request: BalanceRequestDTO,
    db: Session = Depends(get_db)
):
    """
    CONSULTAR BALANCE STELLAR
    
    Obtiene balance de empresa en Stellar.
    
    QUE HACE:
    - Busca empresa por ID
    - Consulta balance XOCHI
    - Consulta balance XLM
    - Verifica cuenta existe
    
    COMO USAR:
    1. Poner empresa_id
    2. Llamar endpoint
    3. Ver balances en respuesta
    
    RESPUESTA:
    - success: true/false
    - xochi_balance: Balance XOCHI
    - xlm_balance: Balance XLM
    - account_exists: true si existe
    """
    try:
        service = PaymentService(db)
        result = service.get_empresa_balance(balance_request.empresa_id)
        return BalanceResponseDTO(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener balance: {str(e)}"
        )

@router.get("/stellar/info")
async def obtener_info_stellar():
    """
    INFORMACION STELLAR
    
    Obtiene informacion de la red Stellar configurada.
    
    QUE HACE:
    - Muestra URL de Horizon
    - Muestra red configurada
    - Muestra claves publicas
    - Muestra asset configurado
    
    COMO USAR:
    1. Llamar GET sin parametros
    2. Ver configuracion actual
    
    RESPUESTA:
    - horizon_url: URL de Horizon
    - network: testnet/mainnet
    - asset_name: XOCHI
    - government_public_key: Clave del gobierno
    - treasury_public_key: Clave de tesoreria
    """
    from ..shared.config import settings
    
    return {
        "horizon_url": settings.HORIZON_URL,
        "network": settings.STELLAR_NETWORK,
        "asset_name": settings.ASSET_NAME,
        "government_public_key": settings.GOVERNMENT_PUBLIC_KEY,
        "treasury_public_key": settings.TREASURY_PUBLIC_KEY
    }
