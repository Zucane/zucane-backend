from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import config
from pydantic import BaseModel
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import BadRequestError, BadResponseError, NotFoundError
import mysql.connector
from mysql.connector import Error as MySQLError
from fastapi import APIRouter, Depends, HTTPException, status, Query
import generate_invoice_pdf
app = FastAPI()
server = Server(horizon_url="https://horizon-testnet.stellar.org")
import os

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END OF CORS BLOCK ---

class PurchaseRequest(BaseModel):
    asset_amount: float
    business_private_key: str

class GetBalanceRequest(BaseModel):
    account_public_key: str

class IssueRequest(BaseModel):
    amount: float
    issuer_private_key: str

# --- NEW: Helper function to get DB connection ---
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
    treasury_keypair = Keypair.from_secret(config.TREASURY_S)

    xlm_to_send = request.asset_amount * config.ZUCOIN_PRICE_IN_XLM

    try:
        send_payment(source_keypair= business_keypair, receiver_public_key=config.TREASURY_P,
                     amount = str(xlm_to_send))
    except (BadRequestError, BadResponseError) as e:
        print("TRANSACTION FAILED AT SENDING PAYMENT")
        print(e)
        raise HTTPException(status_code=400, detail=f"Stellar error when sending XLM: {e}")
    except Exception as e:
        print("UNEXPECTED ERROR AT SENDING PAYMENT")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


    try:
        asset = Asset(config.ASSET_NAME, config.ISSUER_P)
        response = send_payment(source_keypair = treasury_keypair, receiver_public_key=business_keypair.public_key,
                     asset =asset,amount = str(request.asset_amount))

    except (BadRequestError, BadResponseError) as e:
        print("TRANSACTION FAILED AT SENDING TOKENS")
        print(e)
        raise HTTPException(status_code=400, detail=f"Error when sending {config.ASSET_NAME}: {e}")
    except Exception as e:
        print("UNEXPECTED ERROR AT SENDING TOKENS")
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    id_transaction_stellar = response['hash']

    asset_to_XLM = request.asset_amount * config.ZUCOIN_PRICE_IN_XLM
    asset_to_MXN = asset_to_XLM * config.XLM_TO_MXN_RATE
    pdf_path = generate_invoice_pdf.generate_pdf(config.ASSET_NAME,
                                                 request.asset_amount, asset_to_MXN, id_transaction_stellar)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="File not found")

        # 2. Devuelve el archivo
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"purchase_invoice.pdf"
    )

@app.get("/api/business/balance")
def get_business_balance(account_public_key: str):
    asset_balance = 0

    if account_public_key not in config.BUSINESS_DB:
        raise HTTPException(status_code=404, detail="Business not registered.")

    try:
        account_data = server.accounts().account_id(account_public_key).call()
        for balance in account_data['balances']:
            if not balance['asset_type'] == "native" and balance['asset_code'] == config.ASSET_NAME:
                asset_balance = balance['balance']

        asset_balance = float(asset_balance)
        asset_to_XLM = asset_balance * config.ZUCOIN_PRICE_IN_XLM
        asset_to_MXN = asset_to_XLM * config.XLM_TO_MXN_RATE
        hectares = asset_balance * config.ZUCOIN_TO_HECTARE_RATIO
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
        asset_data = server.accounts().account_id(config.TREASURY_P).call()
        for balance in asset_data['balances']:
            if balance['asset_type'] != "native" and balance['asset_code'] == config.ASSET_NAME and balance['asset_issuer'] == config.ISSUER_P:
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
        treasury_public_key = config.TREASURY_P
        asset = Asset(config.ASSET_NAME, config.ISSUER_P)
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