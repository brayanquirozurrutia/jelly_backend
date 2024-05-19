from django.urls import path
from users.views import UserCreateAPIView

urlpatterns = [
    path('users/create_user/', UserCreateAPIView.as_view(), name='create_user'),
]
