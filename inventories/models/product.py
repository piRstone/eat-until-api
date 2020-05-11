from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from eatuntil.commons.models import TimeStampedModel

from .inventory import Inventory


class Product(TimeStampedModel):
    name = models.CharField(max_length=264)

    expiration_date = models.DateField(
        _('expiration date'))

    notification_delay = models.IntegerField(
        _('notification delay'), default=3)

    inventory = models.ForeignKey(Inventory, verbose_name=_(
        'inventory'), on_delete=models.CASCADE)

    ean13 = models.CharField(_('Code-barre ean13'), max_length=13, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products',
        verbose_name=_('owner'),
        on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)
