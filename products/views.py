from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from products.serializers import GroupSerializer, CategorySerializer, ProductSerializer
from jelly_backend.docs.swagger_tags import PRODUCTS_TAG
from jelly_backend.permissions import IsAdminUserLoggedIn

load_dotenv()


class GroupCreateView(APIView):
    permission_classes = [IsAdminUserLoggedIn]

    @swagger_auto_schema(
        operation_description="""
        ## Create Group
        
        About the endpoint:
        
        - This endpoint creates a new group in the system.
        """,
        operation_id="products_create_group",
        operation_summary="Create Group",
        request_body=GroupSerializer,
        responses={
            201: GroupSerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="""
        ## Create Category
        
        About the endpoint:
        
        - This endpoint creates a new category in the system.
        """,
        operation_summary="Create Category",
        operation_id="products_create_category",
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Create Product

        About the endpoint:

        - This endpoint creates a new product in the system.
        """,
        operation_id="products_create_product",
        operation_summary="Create Product",
        request_body=ProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='image_file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Image of the product'
            )
        ],
        responses={
            201: ProductSerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            serialized_product = ProductSerializer(product).data
            return Response(serialized_product, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
