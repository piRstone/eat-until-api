from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers

from eatuntil.commons.fields import ProtectedFileURLField

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create a new User
        """
        return self.Meta.model.objects.create_user(**validated_data)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                _("That email is already associated to an account"))
        return email


class UserSerializer(serializers.ModelSerializer):

    avatar_thumbnail_url = ProtectedFileURLField(
        'api:user-avatar-thumbnail',
        source='avatar')

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'avatar_thumbnail_url')
