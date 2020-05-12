from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Allow all hosts for dev, @see https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# Allow any password
AUTH_PASSWORD_VALIDATORS = []

PROJECT_BASE_URL = 'http://localhost:8001'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
