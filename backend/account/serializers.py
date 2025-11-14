# Import Dependencies
from rest_framework import serializers

# Import Components
from .models import User, FriendshipRequest

# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends_count', 'posts_count', 'get_avatar',)

class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by')