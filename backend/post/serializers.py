# Import Dependencies
from rest_framework import serializers

# Import Components
from account.serializers import UserSerializer
from post.models import Post



# Create your views here.
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_at_formatted', 'created_by')
