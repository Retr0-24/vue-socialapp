# Import Depnendencies
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#Import Django Dependencies
from django.urls import path

# Configure JWT URL Patterns
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]