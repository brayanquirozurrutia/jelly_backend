from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from jelly_backend.docs.swagger_tags import OUATH_TAG
from oauth2_provider.models import Application
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class CreateOAuthApplicationView(APIView):
    permission_classes = [AllowAny]
    # CAMBIAR PERMISOS A SOLO ADMINISTRADORES
    # permission_classes = [IsAdminUser]
    # CAMBIAR DOCUMENTACIÓN POSTERIOR

    @swagger_auto_schema(
        operation_description="""
        ## Create OAuth2 Application.
        
        About this endpoint:
        
        - No authentication is required to perform this operation.
        
        - This endpoint allows the user to create an OAuth2 application.
        
        - The `name` of the application must be provided in the request body.
        
        - It returns a **JSON** object with the details of the created application.
        """,
        operation_id='Create OAuth2 Application',
        operation_summary='OAuth2 Application',
        tags=OUATH_TAG,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the OAuth2 application',
                ),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Success message',
                    ),
                },
            ),
        },
    )
    def post(self, request):
        name = request.data.get('name')

        if not name or name == '':
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if Application.objects.filter(name=name).exists():
            return Response({'error': 'An application with this name already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        Application.objects.create(
            name=name,
            client_type='confidential',
            authorization_grant_type='password',
        )

        return Response({'message': 'OAuth2 application created successfully'}, status=status.HTTP_200_OK)
