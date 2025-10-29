from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional
from ...shared.database import Base


class AuditoriaTransaccion(Base):
    __tablename__ = "auditoria_transacciones"
    
    auditoria_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaccion_id: Mapped[int] = mapped_column(ForeignKey("transacciones.transaccion_id"), index=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    accion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_accion: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    detalles: Mapped[str] = mapped_column(Text, default="", nullable=False)
    
    # Relaciones
    transaccion: Mapped["Transaccion"] = relationship("Transaccion", back_populates="auditorias")
    
    def __repr__(self):
        return f"<AuditoriaTransaccion(id={self.auditoria_id}, accion={self.accion}, fecha={self.fecha_accion})>"
