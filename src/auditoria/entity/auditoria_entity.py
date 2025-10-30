from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum, func
from datetime import datetime
from typing import Optional
from ...shared.database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"
    
    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(
        Enum("ORDER", "TRANSACTION", "TOKEN", "EMPRESA", name="entity_type"), 
        nullable=False, 
        index=True
    )
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    actor: Mapped[str] = mapped_column(
        Enum("GOV_ADMIN", "COMPANY_USER", "SYSTEM", name="actor_type"), 
        nullable=False, 
        index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stellar_tx_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    detalles: Mapped[str] = mapped_column(Text, default="", nullable=False)
    fecha_accion: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Relaciones comentadas temporalmente para evitar errores de importación
    # transaccion: Mapped[Optional["Transaccion"]] = relationship("Transaccion", back_populates="auditorias")
    
    def __repr__(self):
        return f"<AuditLog(id={self.audit_id}, entity={self.entity_type}, action={self.action}, fecha={self.fecha_accion})>"
