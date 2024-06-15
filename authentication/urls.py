from django.urls import path
from authentication.views import (
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, CSRFTOKENView
)

urlpatterns = [
    path('authentication/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authentication/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('authentication/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('authentication/csrf-token/', CSRFTOKENView.as_view(), name='csrf_token'),
]
