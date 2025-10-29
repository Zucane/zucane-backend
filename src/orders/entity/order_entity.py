from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, Enum, ForeignKey, func
from datetime import datetime
from typing import List
from ...shared.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.empresa_id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "completed", "cancelled", "expired", name="order_status"), 
        default="pending", 
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    transacciones: Mapped[List["Transaccion"]] = relationship("Transaccion", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.order_id}, empresa_id={self.empresa_id}, status={self.status})>"
