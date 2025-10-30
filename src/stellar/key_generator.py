import hashlib
import hmac
from stellar_sdk import Keypair
from typing import Tuple
import base64


class StellarKeyGenerator:
    """
    Generador determinístico de claves Stellar basado en datos de la empresa.
    Usa HMAC-SHA256 para generar claves consistentes a partir de datos únicos.
    """
    
    @staticmethod
    def generate_keypair_from_empresa_data(rfc: str, email: str, nombre: str) -> Tuple[str, str]:
        """
        Genera un par de claves Stellar determinístico basado en datos de la empresa.
        
        Args:
            rfc: RFC de la empresa (13 caracteres)
            email: Email de la empresa
            nombre: Nombre de la empresa
            
        Returns:
            Tuple[str, str]: (public_key, secret_key)
        """
        # Crear una semilla única combinando datos de la empresa
        seed_data = f"{rfc}_{email}_{nombre}".encode('utf-8')
        
        # Usar HMAC-SHA256 para generar una semilla determinística
        # Usar una clave maestra para mayor seguridad
        master_key = b"Zucane_Stellar_Key_Generator_2024"
        seed_hash = hmac.new(master_key, seed_data, hashlib.sha256).digest()
        
        # Usar solo los primeros 32 bytes para el seed de Stellar
        stellar_seed = seed_hash[:32]
        
        # Generar el par de claves usando la semilla
        keypair = Keypair.from_raw_ed25519_seed(stellar_seed)
        
        return keypair.public_key, keypair.secret
    
    @staticmethod
    def generate_keypair_from_user_data(email: str, nombre: str, apellido: str) -> Tuple[str, str]:
        """
        Genera un par de claves Stellar determinístico basado en datos del usuario.
        
        Args:
            email: Email del usuario
            nombre: Nombre del usuario
            apellido: Apellido del usuario
            
        Returns:
            Tuple[str, str]: (public_key, secret_key)
        """
        # Crear una semilla única combinando datos del usuario
        seed_data = f"{email}_{nombre}_{apellido}".encode('utf-8')
        
        # Usar HMAC-SHA256 para generar una semilla determinística
        master_key = b"Zucane_User_Stellar_Key_Generator_2024"
        seed_hash = hmac.new(master_key, seed_data, hashlib.sha256).digest()
        
        # Usar solo los primeros 32 bytes para el seed de Stellar
        stellar_seed = seed_hash[:32]
        
        # Generar el par de claves usando la semilla
        keypair = Keypair.from_raw_ed25519_seed(stellar_seed)
        
        return keypair.public_key, keypair.secret
    
    @staticmethod
    def validate_generated_key(public_key: str) -> bool:
        """
        Valida que una clave generada sea válida.
        
        Args:
            public_key: Clave pública a validar
            
        Returns:
            bool: True si es válida, False si no
        """
        try:
            from stellar_sdk import StrKey
            StrKey.decode_ed25519_public_key(public_key)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_key_info(public_key: str) -> dict:
        """
        Obtiene información sobre una clave generada.
        
        Args:
            public_key: Clave pública
            
        Returns:
            dict: Información de la clave
        """
        try:
            from stellar_sdk import StrKey
            decoded = StrKey.decode_ed25519_public_key(public_key)
            return {
                "valid": True,
                "type": "ed25519",
                "length": len(public_key),
                "starts_with_g": public_key.startswith('G'),
                "decoded_length": len(decoded)
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
