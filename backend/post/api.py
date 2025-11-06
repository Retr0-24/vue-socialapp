# Import Dependencies
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import Components
from .serializers import PostSerializer
from .models import Post
from .forms import PostForm
from account.models import User
from account.serializers import UserSerializer



# Create your views here.
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return Response({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
    })

@api_view(['POST'])
def post_create(request):
    form = PostForm(data=request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
