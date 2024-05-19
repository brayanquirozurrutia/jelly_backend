from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users.serializers import UserSerializer
from jelly_backend.utils.email_utils import SendinblueClient


class UserCreateAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer()},
        operation_description="Create a new user",
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
        sendinblue_client.create_contact(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        # Second we add the contact to the list
        sendinblue_client.add_contact_to_list(
            email_to_add=serializer.validated_data['email'],
        )
        sendinblue_client.activate_account_email(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            activation_code=account_activation_token
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
