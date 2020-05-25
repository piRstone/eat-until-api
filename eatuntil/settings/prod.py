import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

ALLOWED_HOSTS = ['.pirstone.com']

INTERNAL_IPS = ('127.0.0.1',)

CORS_ORIGIN_WHITELIST = [
    'https://eatuntil.pirstone.com',
    '*',
]

LANGUAGE_CODE = 'fr-fr'

try:
    from .local import *
except ImportError:
    pass

sentry_sdk.init(
    dsn=SENTRY_URL,
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
