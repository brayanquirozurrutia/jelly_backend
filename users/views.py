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
from django.middleware.csrf import get_token


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
        user_admin = user.user_admin
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        environment = os.getenv('DJANGO_ENV')

        if environment == 'development':
            secure = False
            same_site = 'Lax'
        else:
            secure = True
            same_site = 'None'

        response = Response({
            'id': user.id,
            'user_admin': user_admin,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=secure,
            samesite=same_site
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=secure,
            samesite=same_site
        )

        return response


class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        ## Logout
        
        About the endpoint:
        
        - This endpoint logs the user out of the system.
        
        - The user will no longer be able to access protected endpoints.""",
        operation_id="Logout",
        tags=USER_TAG,
        operation_summary="Logout",
        responses={204: 'No Content'},
    )
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
