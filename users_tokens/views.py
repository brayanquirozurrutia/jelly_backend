from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users_tokens.serializers import AccountActivationTokenActivateAccountSerializer
from jelly_backend.utils.email_utils import SendinblueClient
from users.models import User
from jelly_backend.docs.swagger_tags import ACCOUNT_ACTIVATION_TOKEN_TAG


class AccountActivationTokenActivateAccountAPIView(APIView):
    serializer_class = AccountActivationTokenActivateAccountSerializer
    permission_classes = [AllowAny]

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
