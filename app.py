from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import config
from pydantic import BaseModel
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import BadRequestError, BadResponseError, NotFoundError
import mysql.connector
from mysql.connector import Error as MySQLError
from fastapi import HTTPException

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

class PurchaseRequest(BaseModel):
    asset_amount: float
    business_private_key: str

class GetBalanceRequest(BaseModel):
    account_public_key: str

class IssueRequest(BaseModel):
    amount: float
    issuer_private_key: str

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        # NEW: Ahora te conectas a tu propia base de datos local
        connection = mysql.connector.connect(
            host="192.168.100.8",          # <-- CAMBIO: 'localhost' es tu propia PC
            user="root",  # <-- CAMBIO: El usuario local que creaste
            password="root", # <-- CAMBIO: La clave local que creaste
            database="zucane_db"    # <-- CAMBIO: El nombre de tu DB local
        )
        return connection
    except MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def send_payment(source_keypair, receiver_public_key, amount:str, asset = Asset.native()):
    source_public_key = source_keypair.public_key
    source_account = server.load_account(source_public_key)

    base_fee = 100
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .add_text_memo("Sending payment ->")  # Add a memo
        .append_payment_op(receiver_public_key, asset, amount)
        .set_timeout(30)  # Make this transaction valid for the next 30 seconds only
        .build()
    )

    transaction.sign(source_keypair)
    response = server.submit_transaction(transaction)

    return response

# --- API ENDPOINTS ---

@app.get("/")
def read_root():
    return {"HACKATHON2025UTEZ": "XOCHI", "status": "online"}

@app.post("/api/business/purchase")
def purchase(request: PurchaseRequest):
    business_keypair = Keypair.from_secret(request.business_private_key)
    treasury_keypair = Keypair.from_secret(settings.TREASURY_S)

    xlm_to_send = request.asset_amount * settings.ZUCOIN_PRICE_IN_XLM

    try:
        send_payment(source_keypair= business_keypair, receiver_public_key=settings.TREASURY_P,
                     amount = str(xlm_to_send))
    except (BadRequestError, BadResponseError) as e:
        print("TRANSACTION FAILED AT SENDING PAYMENT")
        print(e)
        raise HTTPException(status_code=400, detail=f"Stellar error when sending XLM: {e}")
    except Exception as e:
        print("UNEXPECTED ERROR AT SENDING PAYMENT")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


    try:
        asset = Asset(settings.ASSET_NAME, settings.ISSUER_P)
        response = send_payment(source_keypair = treasury_keypair, receiver_public_key=business_keypair.public_key,
                     asset =asset,amount = str(request.asset_amount))

    except (BadRequestError, BadResponseError) as e:
        print("TRANSACTION FAILED AT SENDING TOKENS")
        print(e)
        raise HTTPException(status_code=400, detail=f"Error when sending {settings.ASSET_NAME}: {e}")
    except Exception as e:
        print("UNEXPECTED ERROR AT SENDING TOKENS")
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    id_transaction_stellar = response['hash']

    asset_to_XLM = request.asset_amount * settings.ZUCOIN_PRICE_IN_XLM
    asset_to_MXN = asset_to_XLM * settings.XLM_TO_MXN_RATE
    pdf_path = generate_invoice_pdf.generate_pdf(settings.ASSET_NAME,
                                                 request.asset_amount, asset_to_MXN, id_transaction_stellar)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="File not found")

        # 2. Devuelve el archivo
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"purchase_invoice.pdf"
    )

@app.get("/api/account/balance")
def account_balance(account_public_key: str):
    asset_balance = 0

    try:
        account_data = server.accounts().account_id(account_public_key).call()
        for balance in account_data['balances']:
            if not balance['asset_type'] == "native" and balance['asset_code'] == settings.ASSET_NAME:
                asset_balance = balance['balance']

        asset_balance = float(asset_balance)
        asset_to_XLM = asset_balance * settings.ZUCOIN_PRICE_IN_XLM
        asset_to_MXN = asset_to_XLM * settings.XLM_TO_MXN_RATE
        hectares = asset_balance * settings.ZUCOIN_TO_HECTARE_RATIO
        return {"asset_balance": asset_balance, "asset_to_XLM": asset_to_XLM,
                "asset_to_MXN": asset_to_MXN, "hectares": hectares}

    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Wallet hasn't been funded yet or it doesn't exist."
        )

    except BadRequestError:
        raise HTTPException(
            status_code=404,
            detail="Invalid public key"
        )

    except (ConnectionError, Exception) as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )

@app.get("/api/asset/balance")
def get_asset_balance():
    asset_balance = 0
    try:
        asset_data = server.accounts().account_id(settings.TREASURY_P).call()
        for balance in asset_data['balances']:
            if balance['asset_type'] != "native" and balance['asset_code'] == settings.ASSET_NAME and balance['asset_issuer'] == settings.ISSUER_P:
                asset_balance = balance['balance']

        asset_balance = float(asset_balance)
        return {"asset_balance": asset_balance}

    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found."
        )

    except BadRequestError:
        raise HTTPException(
            status_code=404,
            detail="Invalid public key"
        )

    except (ConnectionError, Exception) as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )

@app.post("/api/government/issue")
def issue_asset(request: IssueRequest):
    try:
        issuer_keypair = Keypair.from_secret(request.issuer_private_key)
        treasury_public_key = settings.TREASURY_P
        asset = Asset(settings.ASSET_NAME, settings.ISSUER_P)
        response = send_payment(
            source_keypair=issuer_keypair,
            receiver_public_key=treasury_public_key,
            asset=asset,
            amount=str(request.amount),
        )
        return {
            "status": "Assets issued successfully",
            "newly_issued_amount": request.amount,
            "destination_account": treasury_public_key,
            "receipt_hash": response['hash']
        }


    except (BadRequestError, BadResponseError) as e:
        print("TRANSACTION FAILED AT ISSUING TOKENS")
        print(e)
        if "op_no_trust" in str(e):
            raise HTTPException(status_code=400,
                                detail="Issuing Error: The Treasury account does not have a trustline for this asset.")

        raise HTTPException(status_code=400, detail=f"Stellar error during issuance: {e}")

    except Exception as e:
        print(f"UNEXPECTED ERROR AT ISSUING TOKENS: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.get("/api/account/history",)
def get_account_history(account_public_key: str ):
    try:
        response = server.payments().for_account(account_public_key).limit(4).order(desc=True).call()
        records = response['_embedded']['records']

        history = []
        for record in records:
            simplified_record = {
                "id": record.get('id'),
                "type": record.get('type'),
                "created_at": record.get('created_at'),
                "transaction_hash": record.get('transaction_hash'),
            }

            if record['type'] == 'payment':
                simplified_record.update({
                    "amount": record.get('amount'),
                    "asset_code": record.get('asset_code', 'XLM'),
                    "from": record.get('from'),
                    "to": record.get('to'),
                })
            elif record['type'] == 'create_account':
                simplified_record.update({
                    "amount": record.get('starting_balance'),
                    "asset_code": "XLM",
                    "from": record.get('funder'),
                    "to": record.get('account'),
                })
            history.append(simplified_record)

        return history

    except NotFoundError:
        raise HTTPException(
            status_code=4404,
            detail="Wallet hasn't been funded yet or it doesn't exist."
        )
    except BadRequestError:
        raise HTTPException(
            status_code=404,
            detail="Invalid public key"
        )
    except (ConnectionError, Exception) as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
