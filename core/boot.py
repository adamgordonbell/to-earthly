from Crypto.Cipher import AES
import os
import base64
import dotenv

# try:
dotenv.load_dotenv()
cipher = AES.new(os.getenv('TO_EARTHLY_AST')[:32].encode(), AES.MODE_ECB)
script_dir = os.path.dirname(os.path.abspath(__file__))
full_filepath = os.path.join(script_dir, "code.py")

with open(full_filepath, 'r') as file:
    encrypted_code = file.read()

padded_code = cipher.decrypt(base64.b64decode(encrypted_code)).decode()
padding_length = ord(padded_code[-1])
original_code = padded_code[:-padding_length]
exec(original_code)
# except Exception as e:
    # dotenv.load_dotenv()