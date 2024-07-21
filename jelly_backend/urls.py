from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import ensure_csrf_cookie

import debug_toolbar

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from graphene_django.views import GraphQLView

from rest_framework.permissions import AllowAny

from jelly_backend import settings


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

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # API
    path('authentication/', include('authentication.urls'), name='authentication'),
    path('users/', include('users.urls'), name='users'),
    path('users-tokens/', include('users_tokens.urls'), name='users_tokens'),
    path('products/', include('products.urls'), name='products'),
    path('admin-app/', include('admin_app.urls'), name='admin_app'),
]

if settings.DEBUG:
    urlpatterns += [
        # Debug
        path("__debug__/", include(debug_toolbar.urls)),
        # Swagger
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
        # GraphQL
        path('graphql', ensure_csrf_cookie(GraphQLView.as_view(graphiql=True))),
    ]

else:
    urlpatterns += [
        path('graphql', (GraphQLView.as_view(graphiql=False))),
    ]
