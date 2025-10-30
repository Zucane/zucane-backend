from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, Enum, ForeignKey, func, UniqueConstraint
from datetime import datetime
from ...shared.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        UniqueConstraint("order_id", "token_id", name="uq_order_token"),
    )
    
    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False, index=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens_co2.token_id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        Enum("reserved", "released", "sold", name="order_item_status"), 
        default="reserved", 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Relaciones
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    token: Mapped["TokenCO2"] = relationship("TokenCO2", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.order_item_id}, order_id={self.order_id}, token_id={self.token_id}, status={self.status})>"
