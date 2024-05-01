from django.urls import path
from oauth_app.views import CreateOAuthApplicationView

urlpatterns = [
    path('create/', CreateOAuthApplicationView.as_view(), name='create_oauth_application'),
]
