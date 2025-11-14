# Import Depnendencies
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import Django Components
from account import api

# Configure Project URL Patterns and include JWT URLs from account/urls.py
urlpatterns = [
    path('api/', include('account.urls')),
    path('api/posts/', include('post.urls')),
    path('api/search/', include('search.urls')),
    path('api/chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
