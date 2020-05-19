from django.views.generic import TemplateView
from django.http import Http404

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from sendfile import sendfile
from sorl.thumbnail import get_thumbnail

from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserTokenSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer)
from .permissions import isOwnerOrAdmin
from .models import User
from .utils import uidb64_decode


def jwt_response_payload_handler(token, user=None, request=None):
    """
    JWT response handler returning the serialized User instance
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class ActivateUserView(TemplateView):
    template_name = 'activation/activation_error.html'

    def get(self, request, *args, **kwargs):
        if (request.GET.get('uid') and request.GET.get('token')):
            try:
                user = User.objects.get(pk=uidb64_decode(request.GET.get('uid')))
                if User.token_generator.check_token(user, request.GET.get('token')):
                    self.template_name = 'activation/activation.html'
                    user.is_active = True
                    user.save()
            except User.DoesNotExist:
                pass
        return super().get(request, *args, **kwargs)


class CreateUserAPIView(CreateAPIView):
    """
    User registration API view
    """
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny, ]

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

        user = serializer.instance
        user.send_activation_link()

        return Response(status=201, headers=headers)


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [isOwnerOrAdmin]

    def get_queryset(self):
        # TODO : filter here !
        return User.objects.all()

    def get_serializer_class(self):
        """
        By using this method, we could returns the proper serializer for schema
        core API docs like Swagger.
        """
        if self.action == 'activate':
            return UserTokenSerializer
        if self.action == 'forgot_password':
            return ForgotPasswordSerializer
        if self.action == 'reset_password':
            return ResetPasswordSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        # default option
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'change_password':
            context['user'] = self.request.user
        return context

    @action(methods=['get'], detail=False, url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])
    def avatar_thumbnail(self, request):
        """
        Returns the avatar thumbnail file
        """
        user = self.get_object()

        if not user.avatar:
            raise Http404

        thumbnail = get_thumbnail(
            user.avatar, '50x50', crop='center', quality=90)
        return sendfile(request, thumbnail.storage.path(thumbnail.name))

    @action(methods=['post'], detail=False, url_path='activate',
            permission_classes=[permissions.AllowAny])
    def activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.context['user']
        user.is_active = True
        user.save()

        return Response(data=UserSerializer(instance=user).data)

    @action(methods=['post'], detail=False, url_path='forgot-password',
            permission_classes=[permissions.AllowAny])
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data['email'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

        try:
            user.send_reset_password_link()
        except Exception as exc:
            raise ValidationError(str(exc))
        else:
            return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='reset-password',
            permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.context['user']
        user.set_password(serializer.data['password1'])
        user.save()
        return Response(status=status.HTTP_200_OK)
