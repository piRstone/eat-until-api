from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Adds created and modified timestamps with database indexes
    """

    created = models.DateTimeField(
        _('created'),
        editable=False,
        auto_now_add=True,
        db_index=True)

    modified = models.DateTimeField(
        _('modified'),
        editable=False,
        auto_now=True,
        db_index=True)

    class Meta:
        abstract = True
