from django.apps import AppConfig
from django.db.models.signals import pre_save


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .signals import set_normalized_email
        from .models import User

        pre_save.connect(set_normalized_email, sender=User)
