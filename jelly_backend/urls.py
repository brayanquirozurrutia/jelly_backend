import debug_toolbar

from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework.permissions import AllowAny

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

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # API
    path(API_VERSION_1, include('oauth_app.urls')),
    path(API_VERSION_1, include('jwt_app.urls')),
    path(API_VERSION_1, include('users.urls')),
    path(API_VERSION_1, include('users_tokens.urls')),
    path(API_VERSION_1, include('products.urls')),
    # Debug
    path("__debug__/", include(debug_toolbar.urls)),
    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # OAuth2
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # GraphQL
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
