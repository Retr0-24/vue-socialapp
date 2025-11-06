# Import Dependencies
from rest_framework import serializers

# Import Components
from .models import User

# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')