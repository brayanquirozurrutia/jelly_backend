from django.urls import path
from jwt_app.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path('jwt/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]
