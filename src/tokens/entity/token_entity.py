from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, DateTime, Enum, func
from datetime import datetime
from typing import List
from ...shared.database import Base


class TokenCO2(Base):
    __tablename__ = "tokens_co2"
    
    token_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad_co2: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_emision: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(
        Enum("emitido", "disponible", "reservado", "vendido", name="token_status"), 
        default="disponible", 
        nullable=False
    )
    
    asset_code: Mapped[str] = mapped_column(String(20), default="ZUCOIN", nullable=False)
    issuer_pubkey: Mapped[str] = mapped_column(String(56), nullable=False)  # GOVERNMENT_PUBLIC_KEY
    dist_pubkey: Mapped[str] = mapped_column(String(56), nullable=False)    # TREASURY_PUBLIC_KEY
    
    # Relaciones comentadas temporalmente para evitar errores de configuración
    # transacciones: Mapped[List["Transaccion"]] = relationship("Transaccion", back_populates="token")
    # order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="token")
    # transaccion_items: Mapped[List["TransaccionItem"]] = relationship("TransaccionItem", back_populates="token")
    
    def __repr__(self):
        return f"<TokenCO2(id={self.token_id}, cantidad={self.cantidad_co2}, status={self.status})>"
