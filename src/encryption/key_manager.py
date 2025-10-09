from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class KeyManager:
    """Manages the generation of a cryptographic key from a password."""
    def __init__(self):
        self._salt = None
        self._key = None

    def generate_key_from_password(self, password: str, salt: bytes = None) -> tuple[bytes, bytes]:
        """
        Derives a key from a password using PBKDF2HMAC.
        If no salt is provided, a new one is generated.
        
        Returns:
            (key, salt)
        """
        self._salt = salt or os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit AES key
            salt=self._salt,
            iterations=100000,
        )
        self._key = kdf.derive(password.encode())
        return self._key, self._salt

    def get_key(self) -> bytes:
        """Returns the derived key."""
        return self._key
