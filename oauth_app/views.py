from drf_yasg import openapi
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from jelly_backend.docs.swagger_tags import OUATH_TAG
from oauth2_provider.models import Application
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth_app.serializers import CreateOAuthApplicationSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser


class CreateOAuthApplicationView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateOAuthApplicationSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Create OAuth2 Application.

        About this endpoint:

        - Authentication as an admin is required to perform this operation.

        - This endpoint allows the user to create an OAuth2 application.

        - The `name` of the application must be provided in the request body.

        - It returns a **JSON** object with the details of the created application.
        """,
        operation_id='Create OAuth2 Application',
        operation_summary='OAuth2 Application',
        tags=[OUATH_TAG],
        request_body=CreateOAuthApplicationSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    'client_id': openapi.Schema(type=openapi.TYPE_STRING, description='Client ID of the application'),
                    'client_secret': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='Client secret of the application'),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if Application.objects.filter(name=data['name']).exists():
            raise ValidationError({'error': 'An application with this name already exists'})

        application = Application.objects.create(
            name=data['name'],
            client_type=data['client_type'],
            authorization_grant_type=data['authorization_grant_type'],
            redirect_uris=data.get('redirect_uris', ''),
        )

        return Response({
            'message': 'OAuth2 application created successfully',
            'client_id': application.client_id,
            'client_secret': application.client_secret
        }, status=status.HTTP_200_OK)
