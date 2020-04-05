from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import List, Product


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'name', 'user')
        extra_kwargs = {
            'user': {'read_only': True,}
        }


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'expiration_date', 'notification_delay', 'inventory', 'user')
        extra_kwargs = {
            'user': {'read_only': True, }
        }
