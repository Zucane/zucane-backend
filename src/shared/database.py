
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crear todas las tablas en la base de datos"""
    try:
        # Importar solo entidades básicas sin relaciones complejas
        from src.auth.entity.user_entity import User
        from src.empresas.entity.empresa_entity import Empresa
        from src.tokens.entity.token_entity import TokenCO2
        from src.transacciones.entity.transaccion_entity import Transaccion
        from src.pagos.entity.pago_entity import PagoProductor
        from src.auditoria.entity.auditoria_entity import AuditLog
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("Base de datos inicializada")
    except Exception as e:
        print(f"Error al inicializar base de datos: {e}")
        raise
