from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from .entity.pago_entity import PagoProductor
from .dto.pago_dto import PagoCreateDTO, PagoUpdateDTO


class PagoRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, pago_data: PagoCreateDTO) -> PagoProductor:
        pago = PagoProductor(**pago_data.dict())
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago
    
    def get_by_id(self, pago_id: int) -> Optional[PagoProductor]:
        return self.db.query(PagoProductor).filter(
            PagoProductor.pago_id == pago_id
        ).first()
    
    def get_by_transaccion(self, transaccion_id: int) -> List[PagoProductor]:
        return self.db.query(PagoProductor).filter(
            PagoProductor.transaccion_id == transaccion_id
        ).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[PagoProductor]:
        return self.db.query(PagoProductor).filter(
            PagoProductor.status == status
        ).offset(skip).limit(limit).all()
    
    def get_pending_payments(self) -> List[PagoProductor]:
        return self.db.query(PagoProductor).filter(
            PagoProductor.status == "pendiente"
        ).all()
    
    def update(self, pago_id: int, pago_data: PagoUpdateDTO) -> Optional[PagoProductor]:
        pago = self.get_by_id(pago_id)
        if not pago:
            return None
        
        update_data = pago_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pago, field, value)
        
        self.db.commit()
        self.db.refresh(pago)
        return pago
    
    def complete_payment(self, pago_id: int, banco: str, cuenta: str) -> Optional[PagoProductor]:
        pago = self.get_by_id(pago_id)
        if not pago:
            return None
        
        pago.status = "completado"
        pago.productor_banco = banco
        pago.productor_cuenta = cuenta
        
        self.db.commit()
        self.db.refresh(pago)
        return pago
    
    def count_by_status(self, status: str) -> int:
        return self.db.query(PagoProductor).filter(PagoProductor.status == status).count()
    
    def count_by_transaccion(self, transaccion_id: int) -> int:
        return self.db.query(PagoProductor).filter(
            PagoProductor.transaccion_id == transaccion_id
        ).count()
    
    def get_total_pending_amount(self) -> float:
        result = self.db.query(PagoProductor.monto).filter(
            PagoProductor.status == "pendiente"
        ).all()
        return sum([float(row[0]) for row in result])
