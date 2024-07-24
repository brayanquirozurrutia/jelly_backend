from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from admin_app.serializers import BannerPhraseSerializer
from jelly_backend.docs.swagger_tags import ADMIN_APP_TAG
from rest_framework.permissions import AllowAny, IsAuthenticated
from admin_app.models import BannerPhrase
from django.core.cache import cache


class CreateBannerPhraseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BannerPhraseSerializer

    @swagger_auto_schema(
        operation_description="""
        Create a new banner phrase.
        The request must contain the following fields:
        - `phrase` (string): The phrase to be displayed in the banner.
        
        The phrase must be unique.
        
        The response will contain the following fields:
        - `id` (int): The ID of the banner phrase.
        - `phrase` (string): The phrase to be displayed in the banner.
        
        The response status code will be 201 if the banner phrase is created successfully.
        """,
        operation_id='create_banner_phrase',
        operation_summary='Create a banner phrase',
        tags=[ADMIN_APP_TAG],
        request_body=serializer_class,
        responses={
            status.HTTP_201_CREATED: serializer_class,
            status.HTTP_400_BAD_REQUEST: 'Invalid data'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('banner_phrases')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateBannerPhraseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BannerPhraseSerializer

    @swagger_auto_schema(
        operation_description="""
        Update a banner phrase.
        
        The request can contain the following fields:
        - `phrase` (string): The phrase to be displayed in the banner.
        
        The response will contain the following fields:
        - `id` (int): The ID of the banner phrase.
        - `phrase` (string): The phrase to be displayed in the banner.
        
        The response status code will be 200 if the banner phrase is updated successfully.
        """,
        operation_id='update_banner_phrase',
        operation_summary='Update a banner phrase',
        tags=[ADMIN_APP_TAG],
        request_body=serializer_class,
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_404_NOT_FOUND: 'Banner phrase not found',
            status.HTTP_400_BAD_REQUEST: 'Invalid data'
        }
    )
    def put(self, request, *args, **kwargs):
        banner_phrase_id = kwargs.get('id')
        try:
            instance = BannerPhrase.objects.get(id=banner_phrase_id)
        except BannerPhrase.DoesNotExist:
            return Response({'error': 'Banner phrase not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('banner_phrases')
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteBannerPhraseAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        Delete a banner phrase.
        
        The response status code will be 204 if the banner phrase is deleted successfully.
        
        If the banner phrase is not found, the response status code will be 404.
        """,
        operation_id='delete_banner_phrase',
        operation_summary='Delete a banner phrase',
        tags=[ADMIN_APP_TAG],
        responses={
            status.HTTP_204_NO_CONTENT: 'Banner phrase deleted',
            status.HTTP_404_NOT_FOUND: 'Banner phrase not found'
        }
    )
    def delete(self, request, *args, **kwargs):
        banner_phrase_id = kwargs.get('id')
        try:
            instance = BannerPhrase.objects.get(id=banner_phrase_id)
        except BannerPhrase.DoesNotExist:
            return Response({'error': 'Banner phrase not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BannerPhraseSerializer()
        serializer.destroy(instance)
        cache.delete('banner_phrases')
        return Response(status=status.HTTP_204_NO_CONTENT)
