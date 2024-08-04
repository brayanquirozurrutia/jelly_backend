from django.urls import path
from products.views import (
    ProductCreateView,
    CreateGroupView,
    CreateCategoryView,
    EditGroupView,
    DeleteGroupView,
    EditCategoryView,
    DeleteCategoryView,
    ProductUpdateView,
    DisableProductView,
    CreateProductImageFileAPIView,
    CreateVersionAPIView,
)

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('groups-create/', CreateGroupView.as_view(), name='group-create'),
    path('categories-create/', CreateCategoryView.as_view(), name='category-create'),
    path('groups-update/<uuid:group_id>/', EditGroupView.as_view(), name='group-edit'),
    path('categories-update/<uuid:category_id>/', EditCategoryView.as_view(), name='category-edit'),
    path('groups-delete/<uuid:group_id>/', DeleteGroupView.as_view(), name='group-delete'),
    path('categories-delete/<uuid:category_id>/', DeleteCategoryView.as_view(), name='category-delete'),
    path('update/<uuid:product_id>/', ProductUpdateView.as_view(), name='product-update'),
    path('disable/<uuid:product_id>/', DisableProductView.as_view(), name='product-disable'),
    path('upload-image/<uuid:product_id>/', CreateProductImageFileAPIView.as_view(), name='upload-image'),
    path('create-version/<uuid:product_id>/', CreateVersionAPIView.as_view(), name='create-version'),
]
