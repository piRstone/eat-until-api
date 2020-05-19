from django.contrib import admin
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetCompleteView)
from django.conf import settings
from django.conf.urls import url, include
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from accounts.views import (
    CreateUserAPIView,
    UserViewSet,
    ActivateUserView)
from inventories.views import InventoryViewSet, ProductViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='users')
router.register(r'inventories', InventoryViewSet, base_name='inventories')
router.register(r'products', ProductViewSet, base_name='products')

api_urls = router.urls
api_urls += [
    url(r'register', CreateUserAPIView.as_view(), name='register'),
    url(r'token-auth', obtain_jwt_token, name='token-auth'),
    url(r'token-refresh', refresh_jwt_token, name='token-refresh'),
    url(r'token-verify', verify_jwt_token, name='token-verify')
]

urlpatterns = [
    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('activation/', ActivateUserView.as_view(), name='activate_user'),
    url(r'admin/', admin.site.urls),
    url(r'api/', include((api_urls, 'api'), namespace='api'))
]

if settings.DEBUG:
    import debug_toolbar

    schema_view = get_schema_view(
        openapi.Info(
            title='Eat Until API',
            default_version='v1',
        ),
        public=False,  # Even if we include doc only for dev, still force user login
        permission_classes=(AllowAny,),
    )

    urlpatterns += [

        url(r'drf/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
        path('__debug__/', include(debug_toolbar.urls)),  # For admin views
    ]

admin.site.site_title = 'Eat Until Administration'
admin.site.site_header = 'Eat Until Administration'
