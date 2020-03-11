from django.http import Http404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from sendfile import sendfile
from sorl.thumbnail import get_thumbnail

from .serializers import (
    CreateUserSerializer,
    UserSerializer)
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    JWT response handler returning the serialized User instance
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class CreateUserAPIView(CreateAPIView):
    """
    User registration API view
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def _get_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        data = {
            'token': self._get_token(serializer.instance)
        }

        return Response(data, status=201, headers=headers)


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        # TODO : filter here !
        return User.objects.all()

    @action(detail=True, methods=['get'])
    def avatar_thumbnail(self, request, pk=None):
        """
        Returns the avatar thumbnail file
        """
        baby = self.get_object()

        if not baby.avatar:
            raise Http404

        thumbnail = get_thumbnail(
            baby.avatar, '50x50', crop='center', quality=90)
        return sendfile(request, thumbnail.storage.path(thumbnail.name))
