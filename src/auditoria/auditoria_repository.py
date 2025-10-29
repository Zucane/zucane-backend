from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from .entity.auditoria_entity import AuditoriaTransaccion
from .dto.auditoria_dto import AuditoriaCreateDTO, AuditoriaUpdateDTO, AuditoriaFiltrosDTO


class AuditoriaRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, auditoria_data: AuditoriaCreateDTO) -> AuditoriaTransaccion:
        auditoria = AuditoriaTransaccion(**auditoria_data.dict())
        self.db.add(auditoria)
        self.db.commit()
        self.db.refresh(auditoria)
        return auditoria
    
    def get_by_id(self, auditoria_id: int) -> Optional[AuditoriaTransaccion]:
        return self.db.query(AuditoriaTransaccion).filter(
            AuditoriaTransaccion.auditoria_id == auditoria_id
        ).first()
    
    def get_by_transaccion(self, transaccion_id: int, skip: int = 0, limit: int = 100) -> List[AuditoriaTransaccion]:
        return self.db.query(AuditoriaTransaccion).filter(
            AuditoriaTransaccion.transaccion_id == transaccion_id
        ).order_by(desc(AuditoriaTransaccion.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[AuditoriaTransaccion]:
        return self.db.query(AuditoriaTransaccion).filter(
            AuditoriaTransaccion.usuario_id == usuario_id
        ).order_by(desc(AuditoriaTransaccion.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_by_filtros(self, filtros: AuditoriaFiltrosDTO, skip: int = 0, limit: int = 100) -> List[AuditoriaTransaccion]:
        query = self.db.query(AuditoriaTransaccion)
        
        if filtros.transaccion_id:
            query = query.filter(AuditoriaTransaccion.transaccion_id == filtros.transaccion_id)
        
        if filtros.usuario_id:
            query = query.filter(AuditoriaTransaccion.usuario_id == filtros.usuario_id)
        
        if filtros.accion:
            query = query.filter(AuditoriaTransaccion.accion.ilike(f"%{filtros.accion}%"))
        
        if filtros.fecha_desde:
            query = query.filter(AuditoriaTransaccion.fecha_accion >= filtros.fecha_desde)
        
        if filtros.fecha_hasta:
            query = query.filter(AuditoriaTransaccion.fecha_accion <= filtros.fecha_hasta)
        
        return query.order_by(desc(AuditoriaTransaccion.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditoriaTransaccion]:
        return self.db.query(AuditoriaTransaccion).order_by(
            desc(AuditoriaTransaccion.fecha_accion)
        ).offset(skip).limit(limit).all()
    
    def update(self, auditoria_id: int, auditoria_data: AuditoriaUpdateDTO) -> Optional[AuditoriaTransaccion]:
        auditoria = self.get_by_id(auditoria_id)
        if not auditoria:
            return None
        
        update_data = auditoria_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(auditoria, field, value)
        
        self.db.commit()
        self.db.refresh(auditoria)
        return auditoria
    
    def count_by_transaccion(self, transaccion_id: int) -> int:
        return self.db.query(AuditoriaTransaccion).filter(
            AuditoriaTransaccion.transaccion_id == transaccion_id
        ).count()
    
    def count_by_usuario(self, usuario_id: int) -> int:
        return self.db.query(AuditoriaTransaccion).filter(
            AuditoriaTransaccion.usuario_id == usuario_id
        ).count()
    
    def count_by_filtros(self, filtros: AuditoriaFiltrosDTO) -> int:
        query = self.db.query(AuditoriaTransaccion)
        
        if filtros.transaccion_id:
            query = query.filter(AuditoriaTransaccion.transaccion_id == filtros.transaccion_id)
        
        if filtros.usuario_id:
            query = query.filter(AuditoriaTransaccion.usuario_id == filtros.usuario_id)
        
        if filtros.accion:
            query = query.filter(AuditoriaTransaccion.accion.ilike(f"%{filtros.accion}%"))
        
        if filtros.fecha_desde:
            query = query.filter(AuditoriaTransaccion.fecha_accion >= filtros.fecha_desde)
        
        if filtros.fecha_hasta:
            query = query.filter(AuditoriaTransaccion.fecha_accion <= filtros.fecha_hasta)
        
        return query.count()
    
    def get_total_count(self) -> int:
        return self.db.query(AuditoriaTransaccion).count()
