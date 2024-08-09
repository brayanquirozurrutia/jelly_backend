
from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema, logger
from drf_yasg import openapi
from products.serializers import (
    CreateGroupSerializer,
    UpdateGroupSerializer,
    DeleteGroupSerializer,
    CreateCategorySerializer,
    UpdateCategorySerializer,
    ProductSerializer,
    DeleteCategorySerializer,
    ProductImageFileSerializer,
    VersionSerializer,
)
from jelly_backend.docs.swagger_tags import PRODUCTS_TAG
from jelly_backend.permissions import IsAdminUserLoggedIn
from products.models import Group, Category, Product

load_dotenv()


class CreateGroupView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = CreateGroupSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Create Group
        
        About the endpoint:
        
        - This endpoint creates a new group in the system.
        """,
        operation_id="products_create_group",
        operation_summary="Create Group",
        request_body=CreateGroupSerializer,
        responses={
            201: CreateGroupSerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateCategoryView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = CreateCategorySerializer

    @swagger_auto_schema(
        operation_description="""
        ## Create Category

        About the endpoint:

        - This endpoint creates a new category in the system.
        """,
        operation_id="products_create_category",
        operation_summary="Create Category",
        request_body=CreateCategorySerializer,
        responses={
            201: CreateCategorySerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EditGroupView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = UpdateGroupSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Edit Group

        About the endpoint:

        - This endpoint edits an existing group in the system.
        """,
        operation_id="products_edit_group",
        operation_summary="Edit Group",
        request_body=UpdateGroupSerializer,
        responses={
            200: UpdateGroupSerializer,
            400: 'Bad Request',
            404: 'Group not found',
        },
        tags=[PRODUCTS_TAG]
    )
    def patch(self, request, group_id):
        group_obj = Group.objects.filter(id=group_id).first()
        serializer = self.serializer_class(data=request.data, instance=group_obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(serializer.instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditCategoryView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = UpdateCategorySerializer

    @swagger_auto_schema(
        operation_description="""
        ## Edit Category

        About the endpoint:

        - This endpoint edits an existing category in the system.
        """,
        operation_id="products_edit_category",
        operation_summary="Edit Category",
        request_body=UpdateCategorySerializer,
        responses={
            200: UpdateCategorySerializer,
            400: 'Bad Request',
            404: 'Category not found',
        },
        tags=[PRODUCTS_TAG]
    )
    def patch(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id).first()
        serializer = self.serializer_class(data=request.data, instance=category_obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(serializer.instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteGroupView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = DeleteGroupSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Delete Group
        
        About the endpoint:
        
        - This endpoint deletes an existing group in the system.
        """,
        operation_id="products_delete_group",
        operation_summary="Delete Group",
        responses={
            200: 'Group deleted successfully.',
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def delete(self, request, group_id):
        serializer = self.serializer_class(data={'group_id': group_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response('Group deleted successfully.', status=status.HTTP_200_OK)


class DeleteCategoryView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = DeleteCategorySerializer

    @swagger_auto_schema(
        operation_description="""
        ## Delete Category

        About the endpoint:

        - This endpoint deletes an existing category in the system.
        """,
        operation_id="products_delete_category",
        operation_summary="Delete Category",
        responses={
            200: 'Category deleted successfully.',
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def delete(self, request, category_id):
        serializer = self.serializer_class(data={'category_id': category_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response('Category deleted successfully.', status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
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


class ProductUpdateView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Update Product

        About the endpoint:

        - This endpoint updates an existing product in the system.
        """,
        operation_id="products_update_product",
        operation_summary="Update Product",
        request_body=ProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='image_file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description='Updated image of the product (optional)'
            ),
            openapi.Parameter(
                name='product_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='ID of the product to be updated'
            )
        ],
        responses={
            200: ProductSerializer,
            400: 'Bad Request',
            404: 'Not Found',
        },
        tags=[PRODUCTS_TAG]
    )
    def patch(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_id'])
        except Product.DoesNotExist:
            return Response({"message": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            data=request.data,
            instance=product,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.update(product, serializer.validated_data)
        serialized_product = ProductSerializer(product).data
        return Response(serialized_product, status=status.HTTP_200_OK)


class DisableProductView(APIView):
    permission_classes = [IsAdminUserLoggedIn]

    @swagger_auto_schema(
        operation_description="""
        ## Disable Product

        About the endpoint:

        - This endpoint disables an existing product in the system.
        """,
        operation_id="products_disable_product",
        operation_summary="Disable Product",
        responses={
            200: 'Product disabled successfully.',
            400: 'Bad Request',
            404: 'Not Found',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if product.is_disabled:
            return Response({"message": "Producto ya está deshabilitado"}, status=status.HTTP_400_BAD_REQUEST)

        product.is_disabled = True
        product.save()
        return Response('Producto deshabilitado exitosamente', status=status.HTTP_200_OK)


class CreateProductImageFileAPIView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductImageFileSerializer

    @swagger_auto_schema(
        operation_description="""
        ## Create Product Image File

        About the endpoint:

        - This endpoint creates a new image file for a product in the system.
        """,
        operation_id="products_create_product_image_file",
        operation_summary="Create Product Image File",
        request_body=ProductImageFileSerializer,
        responses={
            201: 'Image file created successfully.',
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        serializer = self.serializer_class(
            data=request.data, context={
                'request': request,
                'product_id': product_id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateVersionAPIView(APIView):
    permission_classes = [IsAdminUserLoggedIn]
    serializer_class = VersionSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="""
        ## Create Version

        About the endpoint:

        - This endpoint creates a new version in the system.
        """,
        operation_id="products_create_version",
        operation_summary="Create Version",
        request_body=VersionSerializer,
        responses={
            201: VersionSerializer,
            400: 'Bad Request',
        },
        tags=[PRODUCTS_TAG]
    )
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        serializer = self.serializer_class(
            data=request.data, context={
                'request': request,
                'product_id': product_id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
