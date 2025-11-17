# Import Dependencies
from django.urls import path

# Import Componenents
from . import api


urlpatterns = [
    path('', api.notifications, name='notifications'),
]