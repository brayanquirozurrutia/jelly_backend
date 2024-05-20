from django.urls import path
from users_tokens.views import (
    AccountActivationTokenActivateAccountAPIView, AccountActivationTokenNewTokenAPIView,
    PasswordResetTokenNewTokenAPIView, PasswordResetTokenPasswordChangedAPIView
)

urlpatterns = [
    path('activate_account_token/activate_account', AccountActivationTokenActivateAccountAPIView.as_view(),
         name='activate_account'),
    path('activate_account_token/new_token', AccountActivationTokenNewTokenAPIView.as_view(),
         name='activate_account_token_new_token'),
    path('password_reset_token/new_token', PasswordResetTokenNewTokenAPIView.as_view(),
         name='password_reset_token_new_token'),
    path('password_reset_token/password_changed', PasswordResetTokenPasswordChangedAPIView.as_view(),
         name='password_reset_token_password_changed'),
]
