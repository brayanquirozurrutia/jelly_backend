from django.urls import path
from users_tokens.views import AccountActivationTokenActivateAccountAPIView, AccountActivationTokenNewTokenAPIView

urlpatterns = [
    path('activate_account_token/activate_account', AccountActivationTokenActivateAccountAPIView.as_view(),
         name='activate_account'),
    path('activate_account_token/new_token', AccountActivationTokenNewTokenAPIView.as_view(),
            name='new_token'),
]
