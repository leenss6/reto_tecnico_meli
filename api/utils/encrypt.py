from cryptography.fernet import Fernet
import binascii
import os

# Obtiene la clave de encriptación del entorno
key = os.environ.get('ENCRYPT_KEY')
cipher_suite = Fernet(key)

def encrypt_data(data):
    # Encripta los datos
    if not data:
        return None
    return cipher_suite.encrypt(data.encode())

def decrypt_data(data):
    # Desencripta los datos
    if not data:
        return None
    return cipher_suite.decrypt(data).decode()