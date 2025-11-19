# Import Dependencies
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Import Components
from .models import Post, Like, Comment, Trend
from .forms import PostForm, AttachmentForm
from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from notification.utils import create_notification


# Create your views here.
@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return Response({
        'post': PostDetailSerializer(post).data,
    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    # Allow the owner to see their own private posts; otherwise require friendship.
    if user != request.user and request.user not in user.friends.all():
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if user == request.user or request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False


    return Response({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request,
    })

@api_view(['POST'])
def post_create(request):
    form = PostForm(data=request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by= request.user
        attachment.save()
    else:
        print(attachment_form.errors)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        
        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

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

        notification = create_notification(request, 'post_like', post_id=post.id)

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

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return Response({'message': 'Post deleted'})

@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()
    
    return Response({'message': 'Post reported'})


@api_view(['GET'])
def get_trends(request):
     serializer = TrendSerializer(Trend.objects.all(), many=True)

     return Response(serializer.data)
