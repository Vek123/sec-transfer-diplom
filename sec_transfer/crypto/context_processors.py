__all__ = ()

from crypto.utils import RSA_PUBLIC_KEY_COOKIE_NAME


def rsa(request):
    return {
        'RSA_PUBLIC_KEY_COOKIE_NAME': RSA_PUBLIC_KEY_COOKIE_NAME,
    }
