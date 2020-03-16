from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from eatuntil.commons.models import TimeStampedModel


class Product(TimeStampedModel):
    name = models.CharField(max_length=264)

    expiration_date = models.DateField(
        _('expiration date'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products',
        verbose_name=_('owner'),
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ListManager(models.Manager):

    def owner_by(self, user):
        return self\
            .filter(Q(user=user))\
            .order_by('pk')\
            .distinct('pk')


class List(TimeStampedModel):
    name = models.CharField(max_length=264)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='lists',
        verbose_name=_('owner'),
        on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, related_name='products')

    objects = ListManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('api:list-detail', args=[self.pk])
