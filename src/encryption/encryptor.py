import os
import json
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from utils.image_loader import load_image, save_image

def encrypt_image(image_path: str, output_path: str, key: bytes, salt: bytes):
    """
    Encrypts an image using AES-CFB, stores IV + salt in metadata.

    Args:
        image_path: Path to input image.
        output_path: Path to save encrypted file.
        key: Encryption key (bytes).
        salt: Salt used for key derivation.
    """
    image_array, mode = load_image(image_path)
    if image_array is None or mode is None:
        raise ValueError("Failed to load image.")

    data = image_array.tobytes()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    metadata = {
        "shape": image_array.shape,
        "mode": mode,
        "iv": iv.hex(),
        "salt": salt.hex()   # Store salt for decryption
    }

    metadata_json = json.dumps(metadata)
    padded_metadata = metadata_json.ljust(512, ' ').encode('utf-8')

    final_file_data = padded_metadata + encrypted_data

    with open(output_path, 'wb') as f:
        f.write(final_file_data)

    print(f"✅ Image encrypted successfully: {output_path}")
