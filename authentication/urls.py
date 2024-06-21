from django.urls import path
from authentication.views import (
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, CSRFTOKENView
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('csrf-token/', CSRFTOKENView.as_view(), name='csrf_token'),
]
