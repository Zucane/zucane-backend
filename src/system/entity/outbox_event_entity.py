from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, Enum, func
from datetime import datetime
from typing import Optional
from ...shared.database import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aggregate_type: Mapped[str] = mapped_column(
        Enum("TRANSACTION", "ORDER", "TOKEN", name="aggregate_type"), 
        nullable=False, 
        index=True
    )
    aggregate_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("pending", "sent", "error", name="outbox_status"), 
        default="pending", 
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<OutboxEvent(id={self.event_id}, type={self.event_type}, status={self.status})>"
