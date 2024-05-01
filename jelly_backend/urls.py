import debug_toolbar

from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Jelly API",
        default_version='v1',
        description="API dedicated to queries made by and for Jelly",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="brayanquirozurrutia@gmail.com"),
        license=openapi.License(name="BSD License"),
        x_bearer='jwt'
    ),
    public=True,
    permission_classes=[AllowAny],
)

API_VERSION_1 = "jelly/v1/"

apps_urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION_1, include('oauth_app.urls')),
    path(API_VERSION_1, include('users.urls')),
]

debug_urlpatterns = [
    path(r"__debug__/", include(debug_toolbar.urls)),
]

swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

token_urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

oauth_urlpatterns = [
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = apps_urlpatterns + debug_urlpatterns + swagger_urlpatterns + token_urlpatterns + oauth_urlpatterns
