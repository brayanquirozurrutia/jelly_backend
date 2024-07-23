from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.serializers import (
    UserSerializer, UserLoginSerializer
)
from jelly_backend.docs.swagger_tags import USER_TAG
from jelly_backend import settings
from users.models import User


from rest_framework_simplejwt.tokens import RefreshToken

import os
from dotenv import load_dotenv

from users.tasks import send_activate_account_email

load_dotenv()


class UserCreateAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        ## Create a new user
        
        About the endpoint:
        
        - This endpoint creates a new user in the system. The user will be created with the status of inactive.
        
        - The user will receive an email with a link to activate the account.""",
        operation_id="Create user",
        tags=USER_TAG,
        operation_summary="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer()},
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new user.
        """
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            account_activation_token_obj = serializer.instance.account_activation_token
            account_activation_token = account_activation_token_obj.code
            user_email = serializer.validated_data['email']
            user_full_name = serializer.instance.get_full_name()
            send_activate_account_email.delay(
                email=user_email,
                full_name=user_full_name,
                activate_account_code=account_activation_token
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        ## Login
        
        About the endpoint:
        
        - This endpoint allows a user to login to the system.
        
        - The user must provide their email and password to login.
        
        - The user must have an active account to login.""",
        operation_id="Login",
        tags=USER_TAG,
        operation_summary="Login",
        request_body=UserLoginSerializer,
        responses={200: UserLoginSerializer()},
    )
    def post(self, request, *args, **kwargs):
        """
        Login.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        django_env = os.environ.get('DJANGO_ENV', 'development')

        if django_env == 'development':
            httponly = False
            secure = False
            domain = 'localhost'
        else:
            domain = '.tecitostore.com'
            httponly = True
            secure = True

        response = Response({
            'id': user.id,
            'user_admin': user.user_admin,
        })

        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=httponly,
            secure=secure,
            samesite=None,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            domain=domain
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=httponly,
            secure=secure,
            samesite=None,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            domain=domain
        )

        return response


# PARA TESTEAR COSAS
class ListUsersAPIView(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        ## List users
        
        About the endpoint:
        
        - This endpoint lists all the users in the system.
        
        - The users are listed in a paginated way.""",
        operation_id="List users",
        tags=USER_TAG,
        operation_summary="List users",
        responses={200: UserSerializer(many=True)},
    )
    def list(self, request):
        """
        List users.
        """
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
