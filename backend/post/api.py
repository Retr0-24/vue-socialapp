# Import Dependencies
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Import Components
from .models import Post, Like, Comment, Trend
from .forms import PostForm
from account.models import User
from account.serializers import UserSerializer
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer


# Create your views here.
@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return Response({
        'post': PostDetailSerializer(post).data,
    })


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

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return Response({'message': 'Liked'})
    else:
        return Response({'message': 'Already Liked'})

@api_view(['POST'])
def post_create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comment = Comment.objects.create(
        body=request.data.get('body', '').strip(),
        created_by=request.user
    )

    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    serializer = CommentSerializer(comment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_trends(request):
     serializer = TrendSerializer(Trend.objects.all(), many=True)

     return Response(serializer.data)
