from django.urls import path
from users.views import (
    UserCreateAPIView, UserLoginAPIView
)

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]
