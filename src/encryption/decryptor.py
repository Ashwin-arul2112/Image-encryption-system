import json
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from utils.image_loader import save_image, load_image
from encryption.key_manager import KeyManager

def decrypt_image(encrypted_path: str, output_path: str, password: str):
    """
    Decrypts an AES-CFB encrypted image using the password and stored salt.

    Args:
        encrypted_path: Path to encrypted file.
        output_path: Path to save decrypted image.
        password: Password for key derivation.
    """
    with open(encrypted_path, 'rb') as f:
        file_data = f.read()

    padded_metadata = file_data[:512].decode('utf-8').strip()
    encrypted_content = file_data[512:]

    metadata = json.loads(padded_metadata)
    shape = tuple(metadata['shape'])
    mode = metadata['mode']
    iv = bytes.fromhex(metadata['iv'])
    salt = bytes.fromhex(metadata['salt'])

    key_manager = KeyManager()
    key, _ = key_manager.generate_key_from_password(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_content) + decryptor.finalize()

    decrypted_array = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(shape)
    save_image(decrypted_array, output_path, mode)

    print(f"✅ Image decrypted successfully: {output_path}")
