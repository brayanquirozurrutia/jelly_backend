from django.urls import path
from users.views import (
    UserCreateAPIView, UserLoginAPIView, ListUsersAPIView
)

urlpatterns = [
    path('users/create_user/', UserCreateAPIView.as_view(), name='create_user'),
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
    # PARA TESTEAR COSAS
    path('users/list_users/', ListUsersAPIView.as_view({'get': 'list'}), name='list_users'),
]
