from rest_framework import serializers

from .models import Inventory, Product


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ['created', 'modified', 'id',
                  'name', 'user', 'products_count']
        extra_kwargs = {
            'user': {'read_only': True, }
        }


class InventoryEmptySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = []


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['created', 'modified', 'id', 'name', 'expiration_date',
                  'notification_delay', 'inventory', 'ean13', 'user']
        extra_kwargs = {
            'user': {'read_only': True, }
        }
