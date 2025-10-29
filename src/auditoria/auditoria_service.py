from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .entity.auditoria_entity import AuditLog
from .dto.auditoria_dto import (
    AuditoriaCreateDTO, 
    AuditoriaUpdateDTO, 
    AuditoriaResponseDTO, 
    AuditoriaListDTO, 
    AuditoriaFiltrosDTO
)
from .auditoria_repository import AuditoriaRepository


def _map_audit_log_to_dto(auditoria: AuditLog) -> AuditoriaResponseDTO:
    """Helper para mapear AuditLog a AuditoriaResponseDTO con compatibilidad"""
    dto_dict = {
        "audit_id": auditoria.audit_id,
        "entity_type": auditoria.entity_type,
        "entity_id": auditoria.entity_id,
        "actor": auditoria.actor,
        "action": auditoria.action,
        "fecha_accion": auditoria.fecha_accion,
        "detalles": auditoria.detalles,
        "idempotency_key": auditoria.idempotency_key,
        "stellar_tx_hash": auditoria.stellar_tx_hash,
        # Campos legacy
        "auditoria_id": auditoria.audit_id,
        "transaccion_id": auditoria.entity_id if auditoria.entity_type == "TRANSACTION" else None,
        "usuario_id": None,
        "accion_legacy": auditoria.action
    }
    return AuditoriaResponseDTO(**dto_dict)


class AuditoriaService:
    
    def __init__(self, db: Session):
        self.repository = AuditoriaRepository(db)
    
    def crear_auditoria(self, auditoria_data: AuditoriaCreateDTO) -> AuditoriaResponseDTO:
        auditoria = self.repository.create(auditoria_data)
        # Mapear a DTO con compatibilidad
        dto_dict = {
            "audit_id": auditoria.audit_id,
            "entity_type": auditoria.entity_type,
            "entity_id": auditoria.entity_id,
            "actor": auditoria.actor,
            "action": auditoria.action,
            "fecha_accion": auditoria.fecha_accion,
            "detalles": auditoria.detalles,
            "idempotency_key": auditoria.idempotency_key,
            "stellar_tx_hash": auditoria.stellar_tx_hash,
            # Campos legacy
            "auditoria_id": auditoria.audit_id,
            "transaccion_id": auditoria.entity_id if auditoria.entity_type == "TRANSACTION" else None,
            "usuario_id": None,
            "accion": auditoria.action
        }
        return AuditoriaResponseDTO(**dto_dict)
    
    def obtener_auditoria(self, auditoria_id: int) -> Optional[AuditoriaResponseDTO]:
        auditoria = self.repository.get_by_id(auditoria_id)
        if not auditoria:
            return None
        return AuditoriaResponseDTO.from_orm(auditoria)
    
    def listar_auditorias_por_transaccion(self, transaccion_id: int, page: int = 1, size: int = 10) -> AuditoriaListDTO:
        skip = (page - 1) * size
        auditorias = self.repository.get_by_transaccion(transaccion_id, skip=skip, limit=size)
        total = self.repository.count_by_transaccion(transaccion_id)
        
        auditorias_dto = [_map_audit_log_to_dto(auditoria) for auditoria in auditorias]
        
        return AuditoriaListDTO(
            auditorias=auditorias_dto,
            total=total,
            page=page,
            size=size
        )
    
    def listar_auditorias_por_usuario(self, usuario_id: int, page: int = 1, size: int = 10) -> AuditoriaListDTO:
        skip = (page - 1) * size
        auditorias = self.repository.get_by_usuario(usuario_id, skip=skip, limit=size)
        total = self.repository.count_by_usuario(usuario_id)
        
        auditorias_dto = [_map_audit_log_to_dto(auditoria) for auditoria in auditorias]
        
        return AuditoriaListDTO(
            auditorias=auditorias_dto,
            total=total,
            page=page,
            size=size
        )
    
    def buscar_auditorias(self, filtros: AuditoriaFiltrosDTO, page: int = 1, size: int = 10) -> AuditoriaListDTO:
        skip = (page - 1) * size
        auditorias = self.repository.get_by_filtros(filtros, skip=skip, limit=size)
        total = self.repository.count_by_filtros(filtros)
        
        auditorias_dto = [_map_audit_log_to_dto(auditoria) for auditoria in auditorias]
        
        return AuditoriaListDTO(
            auditorias=auditorias_dto,
            total=total,
            page=page,
            size=size
        )
    
    def listar_todas_auditorias(self, page: int = 1, size: int = 10) -> AuditoriaListDTO:
        skip = (page - 1) * size
        auditorias = self.repository.get_all(skip=skip, limit=size)
        total = self.repository.get_total_count()
        
        auditorias_dto = [_map_audit_log_to_dto(auditoria) for auditoria in auditorias]
        
        return AuditoriaListDTO(
            auditorias=auditorias_dto,
            total=total,
            page=page,
            size=size
        )
    
    def actualizar_auditoria(self, auditoria_id: int, auditoria_data: AuditoriaUpdateDTO) -> Optional[AuditoriaResponseDTO]:
        auditoria = self.repository.update(auditoria_id, auditoria_data)
        if not auditoria:
            return None
        return _map_audit_log_to_dto(auditoria)
    
    def registrar_accion(self, transaccion_id: int, accion: str, detalles: str = "", usuario_id: Optional[int] = None) -> AuditoriaResponseDTO:
        auditoria_data = AuditoriaCreateDTO(
            transaccion_id=transaccion_id,
            usuario_id=usuario_id,
            accion=accion,
            detalles=detalles
        )
        return self.crear_auditoria(auditoria_data)
    
    def obtener_resumen_auditoria(self) -> dict:
        return {
            "total_auditorias": self.repository.get_total_count(),
            "auditorias_hoy": self.repository.count_by_filtros(
                AuditoriaFiltrosDTO(
                    fecha_desde=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                )
            )
        }
