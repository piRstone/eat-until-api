from rest_framework import permissions, viewsets

from .models import Inventory, Product
from .permissions import InventoryPermission, ProductPermission
from .serializers import InventorySerializer, ProductSerializer


class InventoryViewSet(viewsets.ModelViewSet):

    serializer_class = InventorySerializer
    permission_classes = (permissions.IsAuthenticated, InventoryPermission)

    def get_queryset(self):
        """Return inventories owned by user"""
        return Inventory.objects.owned_by(self.request.user)

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, ProductPermission)

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)
