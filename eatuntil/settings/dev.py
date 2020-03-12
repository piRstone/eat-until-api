from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

# Allow all hosts for dev, @see https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# Allow any password
AUTH_PASSWORD_VALIDATORS = []

try:
    from .local import *
except ImportError:
    pass
