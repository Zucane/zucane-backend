"""
Configuración de Base de Datos Compartida
SQLAlchemy 2.0 + MySQL
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Base para todos los modelos
class Base(DeclarativeBase):
    pass

# Configuración de la base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
DB_NAME = os.getenv("DB_NAME", "zucane_db")

# URL de conexión MySQL
DB_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Configuración del engine
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False,
    expire_on_commit=False
)


def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crear todas las tablas en la base de datos"""
    # Importar todas las entidades para que SQLAlchemy las registre
    from ..auth.entity.usuario_entity import Usuario
    from ..auth.entity.rol_entity import Rol
    from ..auth.entity.usuario_rol_entity import UsuarioRol
    from ..empresas.entity.empresa_entity import Empresa
    from ..tokens.entity.token_entity import TokenCO2
    from ..orders.entity.order_entity import Order
    from ..orders.entity.order_item_entity import OrderItem
    from ..transacciones.entity.transaccion_entity import Transaccion
    from ..transacciones.entity.transaccion_item_entity import TransaccionItem
    from ..pagos.entity.pago_entity import PagoProductor
    from ..auditoria.entity.auditoria_entity import AuditLog
    from ..system.entity.idempotency_key_entity import IdempotencyKey
    from ..system.entity.outbox_event_entity import OutboxEvent
    
    Base.metadata.create_all(bind=engine)
