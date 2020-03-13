from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import List


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'name', 'user')
        extra_kwargs = {
            'user': {'read_only': True,}
        }
