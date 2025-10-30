from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.transaccion_entity import Transaccion
from .dto.transaccion_dto import TransaccionCreateDTO, TransaccionUpdateDTO, TransaccionResponseDTO, TransaccionListDTO, TransaccionConfirmarDTO
from .transaccion_repository import TransaccionRepository
from ..empresas.empresa_service import EmpresaService
from ..tokens.token_service import TokenService
from ..payments.payment_service import PaymentService


class TransaccionService:
    
    def __init__(self, db: Session):
        self.repository = TransaccionRepository(db)
        self.empresa_service = EmpresaService(db)
        self.token_service = TokenService(db)
        self.payment_service = PaymentService(db)
    
    def crear_transaccion(self, transaccion_data: TransaccionCreateDTO) -> TransaccionResponseDTO:
        # Validar que la empresa esté activa
        if not self.empresa_service.validar_empresa_activa(transaccion_data.empresa_id):
            raise ValueError("La empresa no está activa")
        
        # Validar que el token esté disponible
        token = self.token_service.obtener_token(transaccion_data.token_id)
        if not token or token.status != "disponible":
            raise ValueError("El token no está disponible")
        
        # Crear la transacción
        transaccion = self.repository.create(transaccion_data)
        
        # Reservar el token
        from ..tokens.dto.token_dto import TokenReservaDTO
        reserva_data = TokenReservaDTO(
            token_ids=[transaccion_data.token_id],
            empresa_id=transaccion_data.empresa_id
        )
        self.token_service.reservar_tokens(reserva_data)
        
        return TransaccionResponseDTO.model_validate(transaccion)
    
    def obtener_transaccion(self, transaccion_id: int) -> Optional[TransaccionResponseDTO]:
        transaccion = self.repository.get_by_id(transaccion_id)
        if not transaccion:
            return None
        return TransaccionResponseDTO.model_validate(transaccion)
    
    def listar_transacciones_empresa(self, empresa_id: int, page: int = 1, size: int = 10) -> TransaccionListDTO:
        skip = (page - 1) * size
        transacciones = self.repository.get_by_empresa(empresa_id, skip=skip, limit=size)
        total = self.repository.count_by_empresa(empresa_id)
        
        transacciones_dto = [TransaccionResponseDTO.model_validate(tx) for tx in transacciones]
        
        return TransaccionListDTO(
            transacciones=transacciones_dto,
            total=total,
            page=page,
            size=size
        )
    
    def listar_transacciones_por_status(self, status: str, page: int = 1, size: int = 10) -> TransaccionListDTO:
        skip = (page - 1) * size
        transacciones = self.repository.get_by_status(status, skip=skip, limit=size)
        total = self.repository.count_by_status(status)
        
        transacciones_dto = [TransaccionResponseDTO.model_validate(tx) for tx in transacciones]
        
        return TransaccionListDTO(
            transacciones=transacciones_dto,
            total=total,
            page=page,
            size=size
        )
    
    def confirmar_transaccion(self, transaccion_id: int, confirmar_data: TransaccionConfirmarDTO) -> Optional[TransaccionResponseDTO]:
        transaccion = self.repository.confirm_transaction(
            transaccion_id, 
            confirmar_data.stellar_tx_hash, 
            confirmar_data.stellar_asset_code
        )
        
        if not transaccion:
            return None
        
        # Marcar token como vendido
        self.token_service.vender_tokens([transaccion.token_id])
        
        return TransaccionResponseDTO.model_validate(transaccion)
    
    def fallar_transaccion(self, transaccion_id: int) -> Optional[TransaccionResponseDTO]:
        transaccion = self.repository.fail_transaction(transaccion_id)
        if not transaccion:
            return None
        
        # Liberar token reservado
        self.token_service.liberar_tokens([transaccion.token_id])
        
        return TransaccionResponseDTO.model_validate(transaccion)
    
    def procesar_pago_stellar(self, transaccion_id: int, empresa_secret_key: str = None) -> dict:
        """Procesar pago real en Stellar Network"""
        transaccion = self.repository.get_by_id(transaccion_id)
        if not transaccion:
            return {"success": False, "error": "Transacción no encontrada"}
        
        if transaccion.status != "pendiente":
            return {"success": False, "error": "La transacción no está pendiente"}
        
        # Obtener datos de la empresa
        empresa = self.empresa_service.obtener_empresa(transaccion.empresa_id)
        if not empresa:
            return {"success": False, "error": "Empresa no encontrada"}
        
        # Procesar pago en Stellar
        payment_result = self.payment_service.process_payment(
            empresa_public_key=empresa.stellar_public_key,
            amount=float(transaccion.monto),
            token_id=transaccion.token_id,
            empresa_secret_key=empresa_secret_key
        )
        
        if payment_result["success"]:
            # Actualizar transacción con datos de Stellar
            updated_transaccion = self.repository.confirm_transaction(
                transaccion_id,
                payment_result["transaction_hash"],
                "XOCHI"  # Asset code
            )
            
            if updated_transaccion:
                # Marcar token como vendido
                self.token_service.vender_tokens([transaccion.token_id])
                
                return {
                    "success": True,
                    "transaction_hash": payment_result["transaction_hash"],
                    "ledger": payment_result.get("ledger"),
                    "transaccion": TransaccionResponseDTO.model_validate(updated_transaccion)
                }
        
        return {
            "success": False,
            "error": payment_result.get("error", "Error al procesar pago")
        }
    
    def verificar_pago_stellar(self, transaction_hash: str) -> dict:
        """Verificar pago en Stellar Network"""
        verification = self.payment_service.verify_payment(transaction_hash)
        return verification
    
    def obtener_balance_empresa(self, empresa_id: int) -> dict:
        """Obtener balance de empresa en Stellar"""
        empresa = self.empresa_service.obtener_empresa(empresa_id)
        if not empresa:
            return {"success": False, "error": "Empresa no encontrada"}
        
        return self.payment_service.get_empresa_balance(empresa.stellar_public_key)
    
    def procesar_transacciones_pendientes(self) -> List[TransaccionResponseDTO]:
        transacciones_pendientes = self.repository.get_pending_transactions()
        # Aquí iría la lógica para procesar con Stellar Network
        return [TransaccionResponseDTO.model_validate(tx) for tx in transacciones_pendientes]
