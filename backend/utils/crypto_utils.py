from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise Exception("FERNET_KEY missing in .env")

cipher = Fernet(FERNET_KEY.encode())


def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


# def decrypt_data(data: str) -> str:
#     return cipher.decrypt(data.encode()).decode()

from cryptography.fernet import InvalidToken

def decrypt_data(data):
    try:
        return cipher.decrypt(data.encode()).decode()
    except (InvalidToken, AttributeError):
        # If not encrypted, return original value
        return data

# from cryptography.fernet import Fernet
# print(Fernet.generate_key().decode())