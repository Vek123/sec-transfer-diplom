__all__ = ()

from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates private RSA key in system environment' # NoQA

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='file path to generated RSA private key.',
        )

    def handle(self, *args, **options):
        self.stdout.write('Private key is generating...')
        file_path = options['file_path']
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                bytes(settings.SECRET_KEY, 'utf-8'),
            ),
        )
        with Path(file_path).open('wb') as pem_out:
            pem_out.write(pem)

        self.stdout.write(
            self.style.SUCCESS('Private key was generated successfully'),
        )
