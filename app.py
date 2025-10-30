from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.shared.database import get_db, create_tables
from src.shared.config import settings

# Importar routers de cada dominio
from src.auth.auth_controller import router as auth_router
from src.empresas.empresa_controller import router as empresas_router
from src.tokens.token_controller import router as tokens_router
from src.transacciones.transaccion_controller import router as transacciones_router
from src.pagos.pago_controller import router as pagos_router
from src.auditoria.auditoria_controller import router as auditoria_router
from src.payments.payment_controller import router as payments_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Zucane Backend API",
    version="1.0.0",
    description="Zucane Backend - Sistema de Tokens de CO2 con integración Stellar",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Zucane Team",
        "email": "contact@zucane.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    tags_metadata=[
        {
            "name": "autenticación",
            "description": "Autenticación y gestión de usuarios",
        },
        {
            "name": "empresas",
            "description": "Gestión de empresas compradoras de tokens de CO2",
        },
        {
            "name": "tokens",
            "description": "Tokens de CO2 emitidos por el gobierno",
        },
        {
            "name": "reservas",
            "description": "Sistema de reservas de tokens con TTL",
        },
        {
            "name": "transacciones",
            "description": "Transacciones de compra/venta de tokens",
        },
        {
            "name": "pagos",
            "description": "Pagos físicos a productores",
        },
        {
            "name": "auditoria",
            "description": "Registros de auditoría del sistema",
        },
        {
            "name": "sistema",
            "description": "Idempotencia y eventos asíncronos",
        },
        {
            "name": "health",
            "description": "Endpoints de salud y estado del sistema",
        },
    ],
)

# Configurar CORS
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://192.168.100.6",
    "http://192.168.100.8",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https?://192\.168\.100\.[0-9]+(?::[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de cada dominio
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(empresas_router, prefix=settings.API_V1_STR)
app.include_router(tokens_router, prefix=settings.API_V1_STR)
app.include_router(transacciones_router, prefix=settings.API_V1_STR)
app.include_router(pagos_router, prefix=settings.API_V1_STR)
app.include_router(auditoria_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando Zucane Backend - Arquitectura por Dominio")
    
    try:
        create_tables()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")


@app.get("/", tags=["health"])
async def root():
    return {
        "message": "Zucane Backend - Sistema de Tokens de CO2",
        "version": "1.0.0",
        "architecture": "Domain-Driven Design",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0",
            "architecture": "Domain-Driven Design",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "version": "1.0.0"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
