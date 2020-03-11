from django.db import models
from django.conf import settings

from eatuntil.commons.models import TimeStampedModel


class List(TimeStampedModel):
  name = models.CharField(max_length=264)

  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='lists',
    verbose_name=_('owner'))

  def __str__(self):
    return self.name
