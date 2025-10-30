from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from .entity.transaccion_entity import Transaccion
from .dto.transaccion_dto import TransaccionCreateDTO, TransaccionUpdateDTO


class TransaccionRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, transaccion_data: TransaccionCreateDTO) -> Transaccion:
        transaccion = Transaccion(**transaccion_data.dict())
        self.db.add(transaccion)
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion
    
    def get_by_id(self, transaccion_id: int) -> Optional[Transaccion]:
        return self.db.query(Transaccion).filter(
            Transaccion.transaccion_id == transaccion_id
        ).first()
    
    def get_by_empresa(self, empresa_id: int, skip: int = 0, limit: int = 100) -> List[Transaccion]:
        return self.db.query(Transaccion).filter(
            Transaccion.empresa_id == empresa_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Transaccion]:
        return self.db.query(Transaccion).filter(
            Transaccion.status == status
        ).offset(skip).limit(limit).all()
    
    def get_by_stellar_hash(self, stellar_tx_hash: str) -> Optional[Transaccion]:
        return self.db.query(Transaccion).filter(
            Transaccion.stellar_tx_hash == stellar_tx_hash
        ).first()
    
    def update(self, transaccion_id: int, transaccion_data: TransaccionUpdateDTO) -> Optional[Transaccion]:
        transaccion = self.get_by_id(transaccion_id)
        if not transaccion:
            return None
        
        update_data = transaccion_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaccion, field, value)
        
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion
    
    def confirm_transaction(self, transaccion_id: int, stellar_tx_hash: str, stellar_asset_code: str) -> Optional[Transaccion]:
        transaccion = self.get_by_id(transaccion_id)
        if not transaccion:
            return None
        
        transaccion.status = "confirmada"
        transaccion.stellar_tx_hash = stellar_tx_hash
        transaccion.stellar_asset_code = stellar_asset_code
        
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion
    
    def fail_transaction(self, transaccion_id: int) -> Optional[Transaccion]:
        transaccion = self.get_by_id(transaccion_id)
        if not transaccion:
            return None
        
        transaccion.status = "fallida"
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion
    
    def count_by_status(self, status: str) -> int:
        return self.db.query(Transaccion).filter(Transaccion.status == status).count()
    
    def count_by_empresa(self, empresa_id: int) -> int:
        return self.db.query(Transaccion).filter(Transaccion.empresa_id == empresa_id).count()
    
    def get_pending_transactions(self) -> List[Transaccion]:
        return self.db.query(Transaccion).filter(
            Transaccion.status == "pendiente"
        ).all()
