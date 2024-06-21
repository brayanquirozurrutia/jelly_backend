from django.urls import path
from users_tokens.views import (
    AccountActivationTokenActivateAccountAPIView, AccountActivationTokenNewTokenAPIView,
    PasswordResetTokenNewTokenAPIView, PasswordResetTokenPasswordChangedAPIView
)

urlpatterns = [
    path('activate-account', AccountActivationTokenActivateAccountAPIView.as_view(),
         name='activate_account'),
    path('activate-account-new_token', AccountActivationTokenNewTokenAPIView.as_view(),
         name='activate_account_token_new_token'),
    path('reset-password-new_token', PasswordResetTokenNewTokenAPIView.as_view(),
         name='password_reset_token_new_token'),
    path('reset-password', PasswordResetTokenPasswordChangedAPIView.as_view(),
         name='password_reset_token_password_changed'),
]
