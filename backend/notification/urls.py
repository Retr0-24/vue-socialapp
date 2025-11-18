# Import Dependencies
from django.urls import path

# Import Componenents
from . import api


urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notification'),
]