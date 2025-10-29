from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func
from datetime import datetime
from ...shared.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    
    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    response_json: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    
    def __repr__(self):
        return f"<IdempotencyKey(key={self.key}, scope={self.scope})>"
