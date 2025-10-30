from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Enum, func
from datetime import datetime
from typing import Optional
from ...shared.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="user_status"), 
        default="active", 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
