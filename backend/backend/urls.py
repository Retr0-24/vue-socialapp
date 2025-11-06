# Import Depnendencies
from account.api import signup
from account import api


# Import Django Components
from django.contrib import admin
from django.urls import path, include

# Configure Project URL Patterns and include JWT URLs from account/urls.py
urlpatterns = [
    path('me/', api.me, name='me'),
    path('api/me/', api.me, name='api-me'),
    path('signup/', api.signup, name='signup'),
    path('api/signup/', api.signup, name='api-signup'),
    path('api/', include('account.urls')),
    path('api/posts/', include('post.urls')),
    path('api/search/', include('search.urls')),
    path('admin/', admin.site.urls),
]
