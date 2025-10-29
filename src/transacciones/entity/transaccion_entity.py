from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, DateTime, Enum, ForeignKey, UniqueConstraint, func
from datetime import datetime
from typing import Optional, List
from ...shared.database import Base


class Transaccion(Base):
    __tablename__ = "transacciones"
    
    transaccion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.empresa_id"), nullable=False, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False, index=True)
    monto: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    fecha_compra: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(
        Enum("pendiente", "confirmada", "fallida", name="tx_status"), 
        default="pendiente", 
        nullable=False
    )
    
    stellar_tx_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, unique=True)
    stellar_asset_code: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    
    # Relaciones
    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="transacciones")
    order: Mapped["Order"] = relationship("Order", back_populates="transacciones")
    transaccion_items: Mapped[List["TransaccionItem"]] = relationship("TransaccionItem", back_populates="transaccion")
    pagos_productores: Mapped[List["PagoProductor"]] = relationship("PagoProductor", back_populates="transaccion")
    auditorias: Mapped[List["AuditoriaTransaccion"]] = relationship("AuditoriaTransaccion", back_populates="transaccion")
    
    def __repr__(self):
        return f"<Transaccion(id={self.transaccion_id}, empresa={self.empresa_id}, token={self.token_id}, status={self.status})>"
