from django.urls import path
from users.views import (
    UserCreateAPIView, UserLoginAPIView, ListUsersAPIView
)

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    # PARA TESTEAR COSAS
    path('list-users/', ListUsersAPIView.as_view({'get': 'list'}), name='list_users'),
]
