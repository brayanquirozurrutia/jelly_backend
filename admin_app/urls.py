from django.urls import path
from admin_app.views import (
    CreateBannerPhraseAPIView, UpdateBannerPhraseAPIView, DeleteBannerPhraseAPIView
)

urlpatterns = [
    path('phrase/create/', CreateBannerPhraseAPIView.as_view(), name='create-banner-phrase'),
    path('phrase/update/<int:id>/', UpdateBannerPhraseAPIView.as_view(), name='update-banner-phrase'),
    path('phrase/delete/<int:id>/', DeleteBannerPhraseAPIView.as_view(), name='delete-banner-phrase'),
]
