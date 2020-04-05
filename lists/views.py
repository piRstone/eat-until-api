from rest_framework import permissions, viewsets

from .models import List, Product
from .permissions import ListPermission
from .serializers import ListSerializer, ProductSerializer


class ListViewSet(viewsets.ModelViewSet):

    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticated, ListPermission)

    def get_queryset(self):
        """Return lists owned by user"""
        return List.objects.owned_by(self.request.user)

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, ListPermission)

    def perform_create(self, serializer):
        """Set the user as owner"""
        serializer.save(user=self.request.user)
