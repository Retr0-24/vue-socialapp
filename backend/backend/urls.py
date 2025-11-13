# Import Depnendencies
from account import api


# Import Django Components
from django.contrib import admin
from django.urls import path, include

# Configure Project URL Patterns and include JWT URLs from account/urls.py
urlpatterns = [
    path('api/', include('account.urls')),
    path('api/posts/', include('post.urls')),
    path('api/search/', include('search.urls')),
    path('api/chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
