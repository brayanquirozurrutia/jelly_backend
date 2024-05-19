from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users_tokens.serializers import (
    AccountActivationTokenActivateAccountSerializer, AccountActivationTokenNewTokenSerializer
)
from jelly_backend.utils.email_utils import SendinblueClient
from users.models import User
from jelly_backend.docs.swagger_tags import ACCOUNT_ACTIVATION_TOKEN_TAG


class AccountActivationTokenActivateAccountAPIView(APIView):
    serializer_class = AccountActivationTokenActivateAccountSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(
        operation_description="""
        ## Activate the account with the token
        
        About the endpoint:
        
        - This endpoint activates the account with the token.
        
        - The user will receive an email with the welcome email.
        
        - The user will receive an email with the account activated email.
        """,
        operation_id="Activate account",
        tags=ACCOUNT_ACTIVATION_TOKEN_TAG,
        operation_summary="Activate the account with the token",
        request_body=AccountActivationTokenActivateAccountSerializer,
        responses={200: "The account has been activated."},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # We send the activation email and the welcome email
        sendinblue_client = SendinblueClient()
        # We get the user
        user_obj = User.objects.get(email=serializer.validated_data['email'])
        first_name = user_obj.first_name
        last_name = user_obj.last_name
        sendinblue_client.send_account_activated_email(
            email=serializer.validated_data['email'],
            first_name=first_name,
            last_name=user_obj.last_name
        )
        sendinblue_client.send_welcome_email(
            email=serializer.validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        return Response("The account has been activated.", status=status.HTTP_200_OK)


class AccountActivationTokenNewTokenAPIView(APIView):
    serializer_class = AccountActivationTokenNewTokenSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        ## Create a new token
        
        About the endpoint:
        
        - This endpoint creates a new token for the account activation.
        
        - The user will receive an email with the new token.
        
        - New token is created when only if the user exists and is registered.
        """,
        operation_id="Create a new token",
        tags=ACCOUNT_ACTIVATION_TOKEN_TAG,
        operation_summary="Create a new token",
        request_body=AccountActivationTokenNewTokenSerializer,
        responses={200: "The new token has been sent."},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        account_activation_token_obj = serializer.instance
        print(account_activation_token_obj)
        if account_activation_token_obj:
            # We send the email with the new token
            sendinblue_client = SendinblueClient()
            # We get the user
            user_obj = account_activation_token_obj.user
            first_name = user_obj.first_name
            sendinblue_client.activate_account_email(
                email=serializer.validated_data['email'],
                first_name=first_name,
                activation_code=account_activation_token_obj.code
            )
            return Response(
                "El token será enviado solamente si el correo es válido y la cuenta aún no ha sido activada",
                status=status.HTTP_200_OK
            )
        return Response(
            "El token será enviado solamente si el correo es válido y la cuenta aún no ha sido activada",
            status=status.HTTP_200_OK
        )
