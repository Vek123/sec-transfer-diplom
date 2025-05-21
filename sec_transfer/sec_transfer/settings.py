from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(BASE_DIR.parent / '.env')

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'secret')

DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.list(
    'DJANGO_ALLOWED_HOSTS',
    default=['127.0.0.1', 'localhost'],
)

INTERNAL_IPS = env.list('DJANGO_INTERNAL_IPS', default=['127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'core.apps.CoreConfig',
    'crypto.apps.CryptoConfig',
    'download.apps.DownloadConfig',
    'homepage.apps.HomepageConfig',
    'storage.apps.StorageConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        'debug_toolbar',
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        *MIDDLEWARE,
    ]

ROOT_URLCONF = 'sec_transfer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'crypto.context_processors.rsa',
            ],
        },
    },
]

WSGI_APPLICATION = 'sec_transfer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'OPTIONS': {
                'pool': True,
            },
            'HOST': env.str('POSTGRES_HOST', 'postgresql'),
            'PORT': env.str('POSTGRES_PORT', '5432'),
            'USER': env.str('POSTGRES_USER', 'user'),
            'PASSWORD': env.str('POSTGRES_PASSWORD', 'password'),
            'NAME': env.str('POSTGRES_DB', 'database'),
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]

TIME_ZONE = 'UTC'
USE_TZ = True

USE_I18N = True
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

FIXTURE_DIRS = [
    BASE_DIR / 'fixtures',
]

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:profile'
LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'users:login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.EmailAuthBackend',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_MAIL = env.str('DJANGO_MAIL', 'default@default.ru')

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = BASE_DIR / 'send_mail'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

RSA_PEM_KEY_FILE = Path(env.str('DJANGO_RSA_PEM_KEY_FILE', 'rsa_key.pem'))

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
