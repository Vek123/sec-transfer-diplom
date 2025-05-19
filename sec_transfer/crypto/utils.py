__all__ = ()

import base64
import contextlib
import os
from pathlib import Path
from typing import Generator

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from django.conf import settings


RSA_ENCRYPT_PADDING = padding.OAEP(
    padding.MGF1(
        hashes.SHA256(),
    ),
    hashes.SHA256(),
    None,
)
RSA_SIGN_PADDING = padding.PSS(
    padding.MGF1(
        hashes.SHA256(),
    ),
    padding.PSS.MAX_LENGTH,
)
RSA_PUBLIC_KEY_COOKIE_NAME = 'public_key'


def encrypt_file(file: bytes) -> tuple[bytes]:
    """Encrypt plaintext with AES and sign AES key with RSA

    Args:
        file (plaintext):

    Returns:
        tuple[bytes,bytes] encrypted_file, aes_key, aes_signature, gcm_tag, iv
    """
    aes_key = os.urandom(32)
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    secret_data = encryptor.update(file) + encryptor.finalize()
    aes_signature = sign_aes_key(aes_key)

    return (secret_data, aes_key, aes_signature, encryptor.tag, iv)


def sign_aes_key(aes_key: bytes) -> bytes:
    with get_private_key() as private_key:
        return private_key.sign(
            aes_key,
            RSA_SIGN_PADDING,
            hashes.SHA256(),
        )


def decrypt_file(
    file: bytes,
    encrypted_aes_key: bytes,
    iv: bytes,
    gcm_tag: bytes,
) -> bytes:
    """Decrypt AES key with RSA and file with decrypted AES key

    Args:
        file (bytes): encrypted text
        encrypted_aes_key (bytes): encrypted AES key with RSA

    Returns:
        bytes: decrypted data
    """
    with get_private_key() as private_key:
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            RSA_ENCRYPT_PADDING,
        )

    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, gcm_tag))
    decryptor = cipher.decryptor()
    return decryptor.update(file) + decryptor.finalize()


def get_public_key() -> rsa.RSAPublicKey:
    with get_private_key() as private_key:
        return private_key.public_key()


@contextlib.contextmanager
def get_private_key() -> Generator[rsa.RSAPrivateKey, None, None]:
    with Path(settings.RSA_PEM_KEY_FILE).open('rb') as key_file:
        yield serialization.load_pem_private_key(
            key_file.read(),
            password=bytes(settings.SECRET_KEY, 'utf-8'),
            backend=default_backend(),
        )


def set_public_key_header():
    public_key = get_public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    public_key = base64.b64encode(public_key)
    return (
        f'{RSA_PUBLIC_KEY_COOKIE_NAME}={public_key}; Path=/; Secure;'
        ' SameSite=None; Partitioned;'
    )


def remove_public_key_header():
    return (
        f'{RSA_PUBLIC_KEY_COOKIE_NAME}=;'
        ' Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/; Secure;'
        ' SameSite=None; Partitioned;'
    )
