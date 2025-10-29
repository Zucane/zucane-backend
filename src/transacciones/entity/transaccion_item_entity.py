from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey, func, UniqueConstraint
from datetime import datetime
from ...shared.database import Base


class TransaccionItem(Base):
    __tablename__ = "transaccion_items"
    __table_args__ = (
        UniqueConstraint("token_id", name="uq_token_sale"),  # Un token solo se vende una vez
    )
    
    tx_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaccion_id: Mapped[int] = mapped_column(ForeignKey("transacciones.transaccion_id"), nullable=False, index=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens_co2.token_id"), nullable=False, index=True)
    precio_unit: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    transaccion: Mapped["Transaccion"] = relationship("Transaccion", back_populates="transaccion_items")
    token: Mapped["TokenCO2"] = relationship("TokenCO2", back_populates="transaccion_items")
    
    def __repr__(self):
        return f"<TransaccionItem(id={self.tx_item_id}, transaccion_id={self.transaccion_id}, token_id={self.token_id}, precio={self.precio_unit})>"
