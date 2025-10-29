from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, DateTime, Enum, ForeignKey, Text, func
from datetime import datetime
from typing import Optional
from ...shared.database import Base


class PagoProductor(Base):
    __tablename__ = "pagos_productores"
    
    pago_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monto: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    transaccion_id: Mapped[int] = mapped_column(ForeignKey("transacciones.transaccion_id"), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("completado", "pendiente", name="pago_status"), 
        default="pendiente", 
        nullable=False
    )
    
    comprobante_pago: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    transaccion: Mapped["Transaccion"] = relationship("Transaccion", back_populates="pagos_productores")
    
    def __repr__(self):
        return f"<PagoProductor(id={self.pago_id}, monto={self.monto}, status={self.status})>"
