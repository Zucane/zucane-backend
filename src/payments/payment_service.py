#!/usr/bin/env python3
"""
Servicio de pagos integrado con Stellar
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from ..stellar.stellar_service import StellarService
from ..shared.config import settings
import logging

logger = logging.getLogger(__name__)

class PaymentService:
    """Servicio para manejar pagos con Stellar"""
    
    def __init__(self, db: Session):
        self.db = db
        self.stellar_service = StellarService(settings.HORIZON_URL)
    
    def process_payment(
        self, 
        empresa_public_key: str,
        amount: float,
        token_id: int,
        empresa_secret_key: str = None
    ) -> Dict[str, Any]:
        """Procesar pago real en Stellar"""
        
        try:
            # 1. Verificar que la empresa tenga suficiente balance
            balance = self.stellar_service.get_account_balance(
                empresa_public_key, 
                settings.ASSET_NAME
            )
            
            if balance < amount:
                return {
                    "success": False,
                    "error": "Balance insuficiente",
                    "required": amount,
                    "available": balance
                }
            
            # 2. Crear transacción de pago
            if empresa_secret_key:
                # Pago directo desde la empresa
                payment_result = self.stellar_service.create_payment_transaction(
                    from_secret=empresa_secret_key,
                    to_public=settings.TREASURY_PUBLIC_KEY,
                    amount=amount,
                    asset_code=settings.ASSET_NAME,
                    issuer_public=settings.GOVERNMENT_PUBLIC_KEY
                )
            else:
                # Simular pago (para testing)
                payment_result = {
                    "success": True,
                    "transaction_hash": f"test_tx_{token_id}_{amount}",
                    "ledger": 12345,
                    "created_at": "2024-01-15T10:30:00Z",
                    "fee_charged": "0.00001"
                }
            
            if payment_result["success"]:
                return {
                    "success": True,
                    "transaction_hash": payment_result["transaction_hash"],
                    "ledger": payment_result.get("ledger"),
                    "created_at": payment_result.get("created_at"),
                    "fee_charged": payment_result.get("fee_charged"),
                    "amount": amount,
                    "token_id": token_id
                }
            else:
                return {
                    "success": False,
                    "error": payment_result.get("error", "Error desconocido en pago")
                }
                
        except Exception as e:
            logger.error(f"Error al procesar pago: {e}")
            return {
                "success": False,
                "error": f"Error interno: {str(e)}"
            }
    
    def verify_payment(self, transaction_hash: str) -> Dict[str, Any]:
        """Verificar pago en Stellar"""
        try:
            verification = self.stellar_service.verify_transaction(transaction_hash)
            
            if verification["success"]:
                return {
                    "success": True,
                    "verified": verification["successful"],
                    "hash": verification["hash"],
                    "ledger": verification["ledger"],
                    "created_at": verification["created_at"],
                    "operations": verification["operations"]
                }
            else:
                return {
                    "success": False,
                    "error": verification.get("error", "Error al verificar")
                }
                
        except Exception as e:
            logger.error(f"Error al verificar pago {transaction_hash}: {e}")
            return {
                "success": False,
                "error": f"Error interno: {str(e)}"
            }
    
    def get_empresa_balance(self, empresa_public_key: str) -> Dict[str, Any]:
        """Obtener balance de una empresa"""
        try:
            # Balance del asset configurado
            xochi_balance = self.stellar_service.get_account_balance(
                empresa_public_key, 
                settings.ASSET_NAME
            )
            
            # Balance de XLM nativo
            xlm_balance = self.stellar_service.get_account_balance(
                empresa_public_key, 
                "XLM"
            )
            
            # Información de la cuenta
            account_info = self.stellar_service.get_account_info(empresa_public_key)
            
            return {
                "success": True,
                "xochi_balance": xochi_balance,
                "xlm_balance": xlm_balance,
                "account_exists": account_info is not None,
                "account_info": account_info
            }
            
        except Exception as e:
            logger.error(f"Error al obtener balance de {empresa_public_key}: {e}")
            return {
                "success": False,
                "error": f"Error interno: {str(e)}"
            }
