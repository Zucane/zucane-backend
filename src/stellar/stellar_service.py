#!/usr/bin/env python3
"""
Servicio para integración real con Stellar Network
"""

from stellar_sdk import Server, Keypair, Network, TransactionBuilder, Asset, Payment
from stellar_sdk.exceptions import NotFoundError, BadRequestError
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class StellarService:
    """Servicio para manejar transacciones reales en Stellar"""
    
    def __init__(self, horizon_url: str = "https://horizon-testnet.stellar.org"):
        self.server = Server(horizon_url)
        self.network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        
    def get_account_info(self, public_key: str) -> Optional[Dict[str, Any]]:
        """Obtener información de una cuenta Stellar"""
        try:
            account = self.server.accounts().account_id(public_key).call()
            return {
                "account_id": account["account_id"],
                "balances": account["balances"],
                "sequence": account["sequence"],
                "subentry_count": account["subentry_count"]
            }
        except NotFoundError:
            logger.warning(f"Cuenta no encontrada: {public_key}")
            return None
        except Exception as e:
            logger.error(f"Error al obtener cuenta {public_key}: {e}")
            return None
    
    def create_payment_transaction(
        self, 
        from_secret: str, 
        to_public: str, 
        amount: float, 
        asset_code: str = "XOCHI",
        issuer_public: str = None
    ) -> Optional[Dict[str, Any]]:
        """Crear transacción de pago en Stellar"""
        try:
            # Crear keypair del emisor
            from_keypair = Keypair.from_secret(from_secret)
            
            # Obtener cuenta del emisor
            from_account = self.server.accounts().account_id(from_keypair.public_key).call()
            
            # Crear asset
            if issuer_public:
                asset = Asset(asset_code, issuer_public)
            else:
                asset = Asset.native()  # XLM nativo
            
            # Crear transacción
            transaction = (
                TransactionBuilder(
                    source_account=from_account,
                    network_passphrase=self.network_passphrase,
                    base_fee=100  # Fee mínimo
                )
                .add_payment_operation(
                    destination=to_public,
                    asset=asset,
                    amount=str(amount)
                )
                .set_timeout(300)  # 5 minutos timeout
                .build()
            )
            
            # Firmar transacción
            transaction.sign(from_keypair)
            
            # Enviar transacción
            response = self.server.submit_transaction(transaction)
            
            if response.get("successful"):
                return {
                    "success": True,
                    "transaction_hash": response["hash"],
                    "ledger": response["ledger"],
                    "created_at": response["created_at"],
                    "fee_charged": response["fee_charged"]
                }
            else:
                logger.error(f"Transacción falló: {response}")
                return {
                    "success": False,
                    "error": response.get("extras", {}).get("result_codes", {})
                }
                
        except NotFoundError:
            logger.error(f"Cuenta emisor no encontrada: {from_keypair.public_key}")
            return {"success": False, "error": "Cuenta emisor no encontrada"}
        except BadRequestError as e:
            logger.error(f"Error en transacción: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_transaction(self, transaction_hash: str) -> Optional[Dict[str, Any]]:
        """Verificar una transacción por su hash"""
        try:
            transaction = self.server.transactions().transaction(transaction_hash).call()
            
            return {
                "success": True,
                "hash": transaction["hash"],
                "ledger": transaction["ledger"],
                "created_at": transaction["created_at"],
                "successful": transaction["successful"],
                "fee_charged": transaction["fee_charged"],
                "operations": transaction["operations"]
            }
        except NotFoundError:
            logger.warning(f"Transacción no encontrada: {transaction_hash}")
            return {"success": False, "error": "Transacción no encontrada"}
        except Exception as e:
            logger.error(f"Error al verificar transacción {transaction_hash}: {e}")
            return {"success": False, "error": str(e)}
    
    def get_account_balance(self, public_key: str, asset_code: str = "XOCHI") -> float:
        """Obtener balance de una cuenta para un asset específico"""
        try:
            account = self.server.accounts().account_id(public_key).call()
            
            for balance in account["balances"]:
                if balance.get("asset_code") == asset_code:
                    return float(balance["balance"])
                elif balance.get("asset_type") == "native":  # XLM
                    return float(balance["balance"])
            
            return 0.0
        except Exception as e:
            logger.error(f"Error al obtener balance de {public_key}: {e}")
            return 0.0
    
    def create_asset_trustline(self, account_secret: str, asset_code: str, issuer_public: str) -> bool:
        """Crear trustline para un asset personalizado"""
        try:
            account_keypair = Keypair.from_secret(account_secret)
            account = self.server.accounts().account_id(account_keypair.public_key).call()
            
            asset = Asset(asset_code, issuer_public)
            
            transaction = (
                TransactionBuilder(
                    source_account=account,
                    network_passphrase=self.network_passphrase,
                    base_fee=100
                )
                .append_change_trust_op(
                    asset=asset,
                    source=account_keypair.public_key
                )
                .set_timeout(300)
                .build()
            )
            
            transaction.sign(account_keypair)
            response = self.server.submit_transaction(transaction)
            
            return response.get("successful", False)
            
        except Exception as e:
            logger.error(f"Error al crear trustline: {e}")
            return False
