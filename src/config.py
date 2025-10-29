import os
from dotenv import load_dotenv

load_dotenv()

GOVERNMENT_P = os.getenv("GOVERNMENT_PUBLIC_KEY")
GOVERNMENT_S = os.getenv("GOVERNMENT_SECRET_KEY")

TREASURY_P = os.getenv("TREASURY_PUBLIC_KEY")
TREASURY_S = os.getenv("TREASURY_SECRET_KEY")

ASSET_NAME = os.getenv("ASSET_NAME", "XOCHI")

HORIZON_URL = os.getenv("HORIZON_URL", "https://horizon-testnet.stellar.org")

