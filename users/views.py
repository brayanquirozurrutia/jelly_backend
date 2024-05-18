from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users.serializers import UserSerializer
from jelly_backend.utils.email_utils import SendinblueClient


@permission_classes([AllowAny])
class UserCreateAPIView(APIView):
    serializer_class = UserSerializer

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
        # We send the welcome email
        sendinblue_client = SendinblueClient()
        sendinblue_client.create_contact(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        sendinblue_client.add_contact_to_list(
            email_to_add=serializer.validated_data['email'],
        )
        sendinblue_client.send_welcome_email(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']

        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
