from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from eatuntil.commons.models import TimeStampedModel

class InventoryManager(models.Manager):

    def owned_by(self, user):
        return self\
            .filter(Q(user=user))\
            .order_by('pk')\
            .distinct('pk')


class Inventory(TimeStampedModel):
    name = models.CharField(max_length=264)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='inventories',
        verbose_name=_('owner'),
        on_delete=models.CASCADE)

    objects = InventoryManager()

    @property
    def products_count(self):
        return self.product_set.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('api:inventory-detail', args=[self.pk])
