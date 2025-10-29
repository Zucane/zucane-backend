"""
QRise Backend - Main Entry Point
Stellar Network Integration for QRise Project
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import config
from src.stellar_setup import establish_trustline, print_and_fund_tokens

def main():
    """Función principal para ejecutar el setup de Stellar"""
    print("🚀 Iniciando QRise Backend - Stellar Setup")
    print(f"📊 Asset: {config.ASSET_NAME}")
    print(f"🏛️  Government: {config.GOVERNMENT_P}")
    print(f"💰 Treasury: {config.TREASURY_P}")
    
    try:
        print("\n🔗 Estableciendo trustline...")
        establish_trustline(config.ASSET_NAME)
        print("✅ Trustline establecido correctamente")
        
        print("\n💰 Imprimiendo y fondeando tokens...")
        response = print_and_fund_tokens(config.ASSET_NAME, "1000000")
        print("✅ Tokens impresos y fondeados correctamente")
        print(f"📋 Respuesta: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
