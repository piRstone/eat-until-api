from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include

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
    UserViewSet)


router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet, base_name='user')

api_urls = router.urls
api_urls = [
    url(r'register', CreateUserAPIView.as_view(), name='register'),
    url(r'token-auth', obtain_jwt_token, name='token-auth'),
    url(r'token-refresh', refresh_jwt_token, name='token-refresh'),
    url(r'token-verify', verify_jwt_token, name='token-verify')
]

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'api/', include(api_urls))
]

if settings.DEBUG:
    # import debug_toolbar

    schema_view = get_schema_view(
        openapi.Info(
            title="Eat Until API",
            default_version='v1',
        ),
        public=False,  # Even if we include doc only for dev, still force user login
        permission_classes=(AllowAny,),
    )

    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),  # For admin views

        # For now, serve API doc only in dev mode. Maybe later should we open
        # it for other company... We'll see when time is coming!
        # path('drf/', include('rest_framework.urls', namespace='rest_framework')),
        # path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
        url(r'swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    ]

admin.site.site_title = 'Eat Until Administration'
admin.site.site_header = 'Eat Until Administration'
