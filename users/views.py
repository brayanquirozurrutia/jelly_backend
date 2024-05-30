from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.serializers import (
    UserSerializer, UserLoginSerializer
)
from jelly_backend.utils.email_utils import SendinblueClient
from jelly_backend.docs.swagger_tags import USER_TAG
from users.models import User


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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO: All the logic to send the email will be with Celery
        # We obtain the activation token
        account_activation_token_obj = serializer.instance.account_activation_token
        account_activation_token = account_activation_token_obj.code
        # We send the activation email
        sendinblue_client = SendinblueClient()
        # First we create the contact in Sendinblue
        user_obj = serializer.instance
        sendinblue_client.create_contact(
            email=serializer.validated_data['email'],
            full_name=user_obj.get_full_name(),
            first_name=user_obj.first_name,
            last_name=user_obj.last_name
        )
        # Second we add the contact to the list
        sendinblue_client.add_contact_to_list(
            email_to_add=serializer.validated_data['email'],
        )
        sendinblue_client.activate_account_email(
            email=serializer.validated_data['email'],
            full_name=user_obj.get_full_name(),
            activation_code=account_activation_token
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
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


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
        return Response(serializer.data)
