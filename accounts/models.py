from django.db import models
from django.db.models import Q
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.fields import ImageField

from eatuntil.commons.storages import PROTECTED_UPLOADS_STORAGE


class UserManager(BaseUserManager):

    def get_by_natural_key(self, email):
        return self.get(email__iexact=self.normalize_email(email))

    def normalize_email(self, email):
        return email.lower()

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User
        """
        if not email:
            raise ValueError("The given email must be set")

        # Normalize email
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)

    def visible_for_user(self, user):
        return (
            self.filter(Q(pk=user.pk) | Q(shares__group__user=user) | Q(shares__group__shared_with=user)) |
            self.filter(pk__in=user.shared_wishlists.values_list('user_id', flat=True))).distinct('pk')


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model
    """

    email = models.EmailField(
        _("email address"),
        unique=True)

    normalized_email = models.CharField(
        _("normalized email address"),
        max_length=254,
        editable=False,
        unique=True)

    avatar = ImageField(
        _('avatar'),
        storage=PROTECTED_UPLOADS_STORAGE,
        upload_to='avatars',
        blank=True)

    is_active = models.BooleanField(
        _("active"),
        default=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def get_short_name(self):
        return self.email
