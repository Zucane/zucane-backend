from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.transaccion_entity import Transaccion
from .dto.transaccion_dto import TransaccionCreateDTO, TransaccionUpdateDTO, TransaccionResponseDTO, TransaccionListDTO, TransaccionConfirmarDTO
from .transaccion_repository import TransaccionRepository
from ..empresas.empresa_service import EmpresaService
from ..tokens.token_service import TokenService


class TransaccionService:
    
    def __init__(self, db: Session):
        self.repository = TransaccionRepository(db)
        self.empresa_service = EmpresaService(db)
        self.token_service = TokenService(db)
    
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
        self.token_service.reservar_tokens({
            "token_ids": [transaccion_data.token_id],
            "empresa_id": transaccion_data.empresa_id
        })
        
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
    
    def procesar_transacciones_pendientes(self) -> List[TransaccionResponseDTO]:
        transacciones_pendientes = self.repository.get_pending_transactions()
        # Aquí iría la lógica para procesar con Stellar Network
        return [TransaccionResponseDTO.model_validate(tx) for tx in transacciones_pendientes]
