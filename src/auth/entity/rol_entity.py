from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, func
from datetime import datetime
from typing import List
from ...shared.database import Base


class Rol(Base):
    __tablename__ = "roles"
    
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    permissions: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Relaciones
    usuario_roles: Mapped[List["UsuarioRol"]] = relationship("UsuarioRol", back_populates="rol")
    
    def __repr__(self):
        return f"<Rol(id={self.role_id}, name={self.role_name})>"
