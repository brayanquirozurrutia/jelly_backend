from django.urls import path
from users.views import (
    UserCreateAPIView, UserLoginAPIView, VerifyICAPIView
)

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('verify-ic/<uuid:user_id>/', VerifyICAPIView.as_view(), name='verify_ic'),
]
