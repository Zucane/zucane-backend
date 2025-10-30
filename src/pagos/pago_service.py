from sqlalchemy.orm import Session
from typing import List, Optional
from .entity.pago_entity import PagoProductor
from .dto.pago_dto import PagoCreateDTO, PagoUpdateDTO, PagoResponseDTO, PagoListDTO, PagoCompletarDTO
from .pago_repository import PagoRepository
from ..transacciones.transaccion_service import TransaccionService


class PagoService:
    
    def __init__(self, db: Session):
        self.repository = PagoRepository(db)
        self.transaccion_service = TransaccionService(db)
    
    def crear_pago(self, pago_data: PagoCreateDTO) -> PagoResponseDTO:
        # Validar que la transacción exista y esté confirmada
        transaccion = self.transaccion_service.obtener_transaccion(pago_data.transaccion_id)
        if not transaccion:
            raise ValueError("La transacción no existe")
        
        if transaccion.status != "confirmada":
            raise ValueError("La transacción debe estar confirmada para crear el pago")
        
        # Crear el pago
        pago = self.repository.create(pago_data)
        return PagoResponseDTO.model_validate(pago)
    
    def obtener_pago(self, pago_id: int) -> Optional[PagoResponseDTO]:
        pago = self.repository.get_by_id(pago_id)
        if not pago:
            return None
        return PagoResponseDTO.model_validate(pago)
    
    def listar_pagos_por_transaccion(self, transaccion_id: int) -> List[PagoResponseDTO]:
        pagos = self.repository.get_by_transaccion(transaccion_id)
        return [PagoResponseDTO.model_validate(pago) for pago in pagos]
    
    def listar_pagos_por_status(self, status: str, page: int = 1, size: int = 10) -> PagoListDTO:
        skip = (page - 1) * size
        pagos = self.repository.get_by_status(status, skip=skip, limit=size)
        total = self.repository.count_by_status(status)
        
        pagos_dto = [PagoResponseDTO.model_validate(pago) for pago in pagos]
        
        return PagoListDTO(
            pagos=pagos_dto,
            total=total,
            page=page,
            size=size
        )
    
    def completar_pago(self, pago_id: int, completar_data: PagoCompletarDTO) -> Optional[PagoResponseDTO]:
        pago = self.repository.complete_payment(
            pago_id, 
            completar_data.productor_banco, 
            completar_data.productor_cuenta
        )
        
        if not pago:
            return None
        
        return PagoResponseDTO.model_validate(pago)
    
    def actualizar_pago(self, pago_id: int, pago_data: PagoUpdateDTO) -> Optional[PagoResponseDTO]:
        pago = self.repository.update(pago_id, pago_data)
        if not pago:
            return None
        return PagoResponseDTO.model_validate(pago)
    
    def obtener_pagos_pendientes(self) -> List[PagoResponseDTO]:
        pagos = self.repository.get_pending_payments()
        return [PagoResponseDTO.model_validate(pago) for pago in pagos]
    
    def obtener_resumen_pagos(self) -> dict:
        return {
            "pendientes": self.repository.count_by_status("pendiente"),
            "completados": self.repository.count_by_status("completado"),
            "monto_total_pendiente": self.repository.get_total_pending_amount()
        }
