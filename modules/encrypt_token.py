from cryptography.fernet import Fernet

# Generar clave (solo una vez)
MASTER_KEY = Fernet.generate_key()
print(f"🔑 MASTER_KEY (GUÁRDALA): {MASTER_KEY.decode()}")

# Datos a encriptar
TOKEN = " "
CHANNEL_ID = " "

# Encriptar
cipher = Fernet(MASTER_KEY)
encrypted_token = cipher.encrypt(TOKEN.encode())
encrypted_channel = cipher.encrypt(CHANNEL_ID.encode())

print(f"🔒 ENCRYPTED_TOKEN: {encrypted_token}")
print(f"🔒 ENCRYPTED_CHANNEL_ID: {encrypted_channel}")