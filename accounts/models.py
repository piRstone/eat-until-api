import logging
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from sorl.thumbnail.fields import ImageField

from eatuntil.commons.storages import PROTECTED_UPLOADS_STORAGE

from .utils import uidb64_encode

logger = logging.getLogger('eatuntil.accounts.users')


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

    token_generator = PasswordResetTokenGenerator()

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

    def _get_frontend_link_token(self, token, path):
        base_url = settings.PROJECT_BASE_URL
        query_params = urlencode({
            # @see django.contribs.auth.forms.PasswordResetForm.save()
            'uid': uidb64_encode(self.pk),
            'token': token,
        })
        return '{}/{}?{}'.format(base_url, path, query_params)

    def get_short_name(self):
        return self.email

    def send_user_email(self, subject_tmpl, body_txt_tmpl, body_html_tmpl, recipients=None, context=None):

        if not recipients:
            if not self.email:
                raise Exception(_('No email send to user "%(user)s" because he has no email.') % {'user': self})
            else:
                recipients = [self.email]

        context = context or {}
        context.update({
            'project_name': settings.PROJECT_NAME,
            'project_email': settings.PROJECT_EMAIL,
            'project_website': settings.PROJECT_WEBSITE,
            'user': self,
        })

        subject = loader.render_to_string(subject_tmpl, context) # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body_txt = loader.render_to_string(body_txt_tmpl, context)
        body_html = loader.render_to_string(body_html_tmpl, context)

        try:
            success = send_mail(
                subject=subject,
                message=body_txt,
                html_message=body_html,
                from_email=None,  # Assume settings.DEFAULT_FROM_EMAIL
                recipient_list=recipients or [self.email],
                fail_silently=False,  # Catch exception for purpose
            )
        except Exception as exc:
            logger.info('An error occured while sending a user email to {} ({}) with exception {}'.format(
                self, self.pk, str(exc)))
            return False
        else:
            return success

    def send_activation_link(self):
        token = self.token_generator.make_token(self)
        context = {
            'activation_link': self._get_frontend_link_token(token, 'activation'),
        }
        success = self.send_user_email(
            subject_tmpl='activation/activation_link_subject.txt',
            body_txt_tmpl='activation/activation_link_body.txt',
            body_html_tmpl='activation/activation_link_body.html',
            context=context,
        )

        if success:
            logger.info('An activation link has been sent to the user {} ({})'.format(self, self.pk))
        else:
            logger.error('An error occured while sending an activation link to the user {} ({})'.format(
                self, self.pk
            ))
            raise Exception(_(
            "An error occured while sending an activation link to %(user)s" % {'user': self}))

    def send_reset_password_link(self):
        token = self.token_generator.make_token(self)
        context = {
            'reset_password_link': self._get_frontend_link_token(token, 'reset-password'),
        }
        success = self.send_user_email(
            subject_tmpl='reset-password/reset_password_link_subject.txt',
            body_txt_tmpl='reset-password/reset_password_link_body.txt',
            body_html_tmpl='reset-password/reset_password_link_body.html',
            context=context,
        )
        if not success:
            logger.error('An error occured while sending an reset password link to the user {} ({})'.format(
                self, self.pk
            ))
            raise Exception(_(
                "An error occured while sending an reset password link to %(user)s" % {'user': self}))
