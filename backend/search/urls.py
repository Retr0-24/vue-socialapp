# Import Dependencies
from django.urls import path

# Import Components
from . import api

urlpatterns = [
    path('', api.search, name='search'),
]