from django.apps import AppConfig
from django.db.models.signals import pre_save


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .signals import set_normalized_email  # pylint: disable=import-outside-toplevel
        from .models import User  # pylint: disable=import-outside-toplevel

        pre_save.connect(set_normalized_email, sender=User)
