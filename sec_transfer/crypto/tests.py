__all__ = ()

import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from django.test import TestCase

from crypto import utils


class CryptoMethodTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_data = b'Hello World!'
        cls.public_key = utils.get_public_key()

    def test_sign_data(self):
        (
            encrypted_data,
            aes_key,
            aes_signature,
            gcm_tag,
            iv,
        ) = utils.encrypt_file(self.test_data)
        self.public_key.verify(
            aes_signature,
            aes_key,
            utils.RSA_SIGN_PADDING,
            hashes.SHA256(),
        )
        decryptor = Cipher(
            algorithms.AES(aes_key), modes.GCM(iv, gcm_tag),
        ).decryptor()
        decrtypted_file = (
            decryptor.update(encrypted_data) + decryptor.finalize()
        )
        self.assertEqual(decrtypted_file, self.test_data)

    def test_decrypt_data(self):
        aes_key = os.urandom(32)
        iv = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(aes_key), modes.GCM(iv),
        ).encryptor()
        encrypted_data = (
            encryptor.update(self.test_data) + encryptor.finalize()
        )
        encrypted_aes_key = self.public_key.encrypt(
            aes_key,
            utils.RSA_ENCRYPT_PADDING,
        )
        decrypted_data = utils.decrypt_file(
            encrypted_data,
            encrypted_aes_key,
            iv,
            encryptor.tag,
        )
        self.assertEqual(decrypted_data, self.test_data)
