from django.urls import path
from products.views import ProductCreateView, GroupCreateView, CategoryCreateView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('groups-create/', GroupCreateView.as_view(), name='group-create'),
    path('categories-create/', CategoryCreateView.as_view(), name='category-create'),
]
