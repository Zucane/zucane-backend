from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, func
from datetime import datetime
from typing import Optional, List
from ...shared.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    
    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[Optional[int]] = mapped_column(ForeignKey("empresas.empresa_id"), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    apellido: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("activo", "inactivo", "bloqueado", name="usuario_status"), 
        default="activo", 
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relaciones comentadas temporalmente para evitar errores
    # empresa: Mapped[Optional["Empresa"]] = relationship("Empresa", back_populates="usuarios")
    # usuario_roles: Mapped[List["UsuarioRol"]] = relationship(
    #     "UsuarioRol", 
    #     foreign_keys="[UsuarioRol.usuario_id]",
    #     back_populates="usuario"
    # )
    
    def __repr__(self):
        return f"<Usuario(id={self.usuario_id}, email={self.email}, empresa_id={self.empresa_id})>"
