from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.pirstone.com']

INTERNAL_IPS = ('127.0.0.1',)

try:
    from .local import *
except ImportError:
    pass
