# backend/app/core/security.py
from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Fernet with the secret key from settings
fernet = Fernet(settings.SECRET_KEY.encode())

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    if not data:
        return data
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string."""
    if not encrypted_data:
        return encrypted_data
    return fernet.decrypt(encrypted_data.encode()).decode()
