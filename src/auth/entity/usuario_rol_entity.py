from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, Enum, ForeignKey, func
from datetime import datetime
from ...shared.database import Base


class UsuarioRol(Base):
    __tablename__ = "usuario_roles"
    
    usuario_role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False)
    assigned_by: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(
        Enum("activo", "inactivo", name="usuario_rol_status"), 
        default="activo", 
        nullable=False
    )
    
    usuario: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[usuario_id], back_populates="usuario_roles")
    rol: Mapped["Rol"] = relationship("Rol", back_populates="usuario_roles")
    assigned_by_user: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[assigned_by])
    
    def __repr__(self):
        return f"<UsuarioRol(usuario_id={self.usuario_id}, role_id={self.role_id}, status={self.status})>"
