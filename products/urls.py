from django.urls import path
from products.views import (
    ProductCreateView,
    CreateGroupView,
    CreateCategoryView,
    EditGroupView,
    DeleteGroupView,
    EditCategoryView,
    DeleteCategoryView,
)

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('groups-create/', CreateGroupView.as_view(), name='group-create'),
    path('categories-create/', CreateCategoryView.as_view(), name='category-create'),
    path('groups-update/<uuid:group_id>/', EditGroupView.as_view(), name='group-edit'),
    path('categories-update/<uuid:category_id>/', EditCategoryView.as_view(), name='category-edit'),
    path('groups-delete/<uuid:group_id>/', DeleteGroupView.as_view(), name='group-delete'),
    path('categories-delete/<uuid:category_id>/', DeleteCategoryView.as_view(), name='category-delete'),
]
