from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from jelly_backend.docs.swagger_tags import JWT_TAG


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token pair.
    """
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="""
        ## JWT Token Pair
        
        This endpoint is used to obtain a JWT token pair.
        """,
        operation_summary="Obtain JWT token pair",
        operation_id="obtain_jwt_token_pair",
        tags=JWT_TAG,
        request_body=TokenObtainPairSerializer,
        responses={200: openapi.Response('Token pair', TokenObtainPairSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh JWT token.
    """
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        operation_description="""
        ## JWT Token Refresh
        
        This endpoint is used to refresh a JWT token.
        """,
        operation_summary="Refresh JWT token",
        operation_id="refresh_jwt_token",
        tags=JWT_TAG,
        request_body=TokenRefreshSerializer,
        responses={200: openapi.Response('Refreshed token', TokenRefreshSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    """
    Verify JWT token.
    """
    serializer_class = TokenVerifySerializer

    @swagger_auto_schema(
        operation_description="""
        ## JWT Token Verify
        
        This endpoint is used to verify a JWT token.
        """,
        operation_summary="Verify JWT token",
        operation_id="verify_jwt_token",
        tags=JWT_TAG,
        request_body=TokenVerifySerializer,
        responses={200: openapi.Response('Verified token', TokenVerifySerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
