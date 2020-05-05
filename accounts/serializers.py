from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from eatuntil.commons.fields import ProtectedFileURLField

from .models import User
from .utils import uidb64_decode


class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'first_name',
            'last_name',
            'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create a new User
        """
        return self.Meta.model.objects.create_user(**validated_data, is_active=False)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                _("That email is already associated to an account"))
        return email


class UserSerializer(ModelSerializer):

    avatar_thumbnail_url = ProtectedFileURLField(
        'api:users-avatar-thumbnail',
        source='avatar')

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar_thumbnail_url')
        extra_kwargs = {
            'email': {'required': True},
        }
        read_only_fields = ['email', 'is_active']


class UserTokenSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True, max_length=255)
    token = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        user_pk = uidb64_decode(attrs['uidb64'])

        try:
            user = User.objects.get(pk=int(user_pk))
        except User.DoesNotExist:
            raise ValidationError({'uidb64': [_('An error occured')]})
        except Exception:
            raise ValidationError({'uidb64': [_('An error occured')]})
        self.context['user'] = user

        if not User.token_generator.check_token(user, attrs['token']):
            raise ValidationError({
                'token': [_('This link has expired. Please ask for a new one.')]
            })

        return super().validate(attrs)


class ResetPasswordSerializer(UserTokenSerializer):
    password1 = serializers.CharField(required=True, max_length=128)
    password2 = serializers.CharField(required=True, max_length=128)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if validated_data['password1'] != validated_data['password2']:
            raise ValidationError(_('Password don\'t match.'))

        try:
            password_validation.validate_password(validated_data['password2'])
        except DjangoValidationError as exc:
            raise ValidationError(str(exc))

        return validated_data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
