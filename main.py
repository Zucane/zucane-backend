
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.shared.config import settings
from src.stellar_setup import establish_trustline, print_and_fund_tokens

def main():
    print("🚀 Iniciando Zucane Backend - Stellar Setup")
    print(f"📊 Asset: {settings.ASSET_NAME}")
    print(f"🏛️  Government: {settings.GOVERNMENT_PUBLIC_KEY}")
    print(f"💰 Treasury: {settings.TREASURY_PUBLIC_KEY}")
    
    try:
        print("\n🔗 Estableciendo trustline...")
        establish_trustline(settings.ASSET_NAME)
        print("✅ Trustline establecido correctamente")
        
        print("\n💰 Imprimiendo y fondeando tokens...")
        response = print_and_fund_tokens(settings.ASSET_NAME, "1000000")
        print("✅ Tokens impresos y fondeados correctamente")
        print(f"📋 Respuesta: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
