# Import Depnendencies
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

#Import Components
from account import api

# Configure JWT URL Patterns
urlpatterns = [
    path('me/', api.me, name='me'),
    path('api/me/', api.me, name='api-me'),
    path('signup/', api.signup, name='signup'),
    path('api/signup/', api.signup, name='api-signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/<uuid:pk>', api.friends, name='friends'),
    path('friends/send-request/<uuid:pk>/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name='handle_request' ),
]