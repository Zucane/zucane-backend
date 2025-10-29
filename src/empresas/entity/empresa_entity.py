from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, Enum, func
from datetime import datetime
from typing import Optional, List
from ...shared.database import Base


class Empresa(Base):
    __tablename__ = "empresas"
    
    empresa_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rfc: Mapped[str] = mapped_column(String(13), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    registro_fecha: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(
        Enum("activo", "inactivo", name="empresa_status"), 
        default="activo", 
        nullable=False
    )
    
    transacciones: Mapped[List["Transaccion"]] = relationship("Transaccion", back_populates="empresa")
    
    def __repr__(self):
        return f"<Empresa(id={self.empresa_id}, rfc={self.rfc}, nombre={self.nombre})>"
