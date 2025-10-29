from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from .entity.auditoria_entity import AuditLog
from .dto.auditoria_dto import AuditoriaCreateDTO, AuditoriaUpdateDTO, AuditoriaFiltrosDTO


class AuditoriaRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, auditoria_data: AuditoriaCreateDTO) -> AuditLog:
        # Mapear DTO antiguo a nueva estructura AuditLog
        audit_log = AuditLog(
            entity_type="TRANSACTION",
            entity_id=auditoria_data.transaccion_id,
            actor="COMPANY_USER" if auditoria_data.usuario_id else "SYSTEM",
            action=auditoria_data.accion,
            detalles=auditoria_data.detalles
        )
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log
    
    def get_by_id(self, auditoria_id: int) -> Optional[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.audit_id == auditoria_id
        ).first()
    
    def get_by_transaccion(self, transaccion_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.entity_type == "TRANSACTION",
            AuditLog.entity_id == transaccion_id
        ).order_by(desc(AuditLog.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        # Nota: AuditLog no tiene usuario_id directo, necesitaríamos ajustar esto
        # Por ahora retornamos todos los logs de COMPANY_USER
        return self.db.query(AuditLog).filter(
            AuditLog.actor == "COMPANY_USER"
        ).order_by(desc(AuditLog.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_by_filtros(self, filtros: AuditoriaFiltrosDTO, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        
        if filtros.transaccion_id:
            query = query.filter(
                AuditLog.entity_type == "TRANSACTION",
                AuditLog.entity_id == filtros.transaccion_id
            )
        
        if filtros.usuario_id:
            # Asumimos COMPANY_USER si hay usuario_id
            query = query.filter(AuditLog.actor == "COMPANY_USER")
        
        if filtros.accion:
            query = query.filter(AuditLog.action.ilike(f"%{filtros.accion}%"))
        
        if filtros.fecha_desde:
            query = query.filter(AuditLog.fecha_accion >= filtros.fecha_desde)
        
        if filtros.fecha_hasta:
            query = query.filter(AuditLog.fecha_accion <= filtros.fecha_hasta)
        
        return query.order_by(desc(AuditLog.fecha_accion)).offset(skip).limit(limit).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(
            desc(AuditLog.fecha_accion)
        ).offset(skip).limit(limit).all()
    
    def update(self, auditoria_id: int, auditoria_data: AuditoriaUpdateDTO) -> Optional[AuditLog]:
        auditoria = self.get_by_id(auditoria_id)
        if not auditoria:
            return None
        
        update_data = auditoria_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(auditoria, field):
                setattr(auditoria, field, value)
        
        self.db.commit()
        self.db.refresh(auditoria)
        return auditoria
    
    def count_by_transaccion(self, transaccion_id: int) -> int:
        return self.db.query(AuditLog).filter(
            AuditLog.entity_type == "TRANSACTION",
            AuditLog.entity_id == transaccion_id
        ).count()
    
    def count_by_usuario(self, usuario_id: int) -> int:
        # Asumimos COMPANY_USER si hay usuario_id
        return self.db.query(AuditLog).filter(
            AuditLog.actor == "COMPANY_USER"
        ).count()
    
    def count_by_filtros(self, filtros: AuditoriaFiltrosDTO) -> int:
        query = self.db.query(AuditLog)
        
        if filtros.transaccion_id:
            query = query.filter(
                AuditLog.entity_type == "TRANSACTION",
                AuditLog.entity_id == filtros.transaccion_id
            )
        
        if filtros.usuario_id:
            query = query.filter(AuditLog.actor == "COMPANY_USER")
        
        if filtros.accion:
            query = query.filter(AuditLog.action.ilike(f"%{filtros.accion}%"))
        
        if filtros.fecha_desde:
            query = query.filter(AuditLog.fecha_accion >= filtros.fecha_desde)
        
        if filtros.fecha_hasta:
            query = query.filter(AuditLog.fecha_accion <= filtros.fecha_hasta)
        
        return query.count()
    
    def get_total_count(self) -> int:
        return self.db.query(AuditLog).count()
