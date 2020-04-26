from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from .models import Inventory, Product
from .permissions import InventoryPermission, ProductPermission
from .serializers import InventorySerializer, ProductSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated, InventoryPermission]

    def get_queryset(self):
        """Return inventories owned by user"""
        return Inventory.objects.owned_by(self.request.user)

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

    def get_queryset(self):
        items = []

        # Filter agains inventory_id ID
        inventory_id = self.request.query_params.get('inventory_id', None)

        if inventory_id is not None:
            items = Product.objects.filter(inventory_id=inventory_id).order_by('expiration_date')

        return items

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)

    def destroy(self, request, pk=None):
        product = None
        try:
            product = Product.objects.get(pk=int(pk))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
