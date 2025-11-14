# Import Dependencies
from rest_framework import serializers

# Import Components
from account.serializers import UserSerializer
from post.models import Post, Comment, Trend



# Create your views here.
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'created_at_formatted', 'created_by')

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'created_at_formatted', 'created_by', 'comments')

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences')