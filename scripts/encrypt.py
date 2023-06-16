from Crypto.Cipher import AES
import base64

# Define the encryption parameters
encryption_key = 'V1Ea945dK6#Hopfu'
cipher = AES.new(encryption_key[:32].encode(), AES.MODE_ECB)

# Read the original code file
with open('./core/boot.py', 'r') as file:
    original_code = file.read()

# Pad the original code to match the AES block size
block_size = 16
padding_length = block_size - (len(original_code) % block_size)
padded_code = original_code + padding_length * chr(padding_length)

# Encrypt the padded code
encrypted_code = base64.b64encode(cipher.encrypt(padded_code.encode())).decode()

# Write the encrypted code to a new file
with open('encrypted_code.py', 'w') as file:
    file.write(encrypted_code)