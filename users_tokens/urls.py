from django.urls import path
from users_tokens.views import AccountActivationTokenActivateAccountAPIView

urlpatterns = [
    path('activate_account_token/activate_account', AccountActivationTokenActivateAccountAPIView.as_view(),
         name='activate_account'),
]
