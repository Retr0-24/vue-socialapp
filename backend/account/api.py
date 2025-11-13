# Import Depnendencies
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Import Components
from .forms import signUpForm
from .models import FriendshipRequest
from .models import User
from .serializers import UserSerializer, FriendshipRequestSerializer


# Create your views here.

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'email': request.user.email,
        'name': request.user.name
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = signUpForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()

        # Send verrification email logic can be added here
    else:
        message = 'Error'

    return JsonResponse({'message': message})

@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)

@api_view(['POST'])
def send_friendship_request(request, pk):
    other_user = get_object_or_404(User, pk=pk)

    if other_user == request.user:
        return JsonResponse({'message': 'You cannot send a request to yourself.'}, status=400)

    if request.user.friends.filter(pk=other_user.pk).exists():
        return JsonResponse({'message': 'You are already friends.'}, status=400)

    reverse_request = FriendshipRequest.objects.filter(
        created_for=request.user,
        created_by=other_user,
        status=FriendshipRequest.SENT,
    ).first()

    if reverse_request:
        reverse_request.status = FriendshipRequest.ACCEPTED
        reverse_request.save(update_fields=['status'])

        request.user.friends.add(other_user)
        request.user.friends_count = request.user.friends.count()
        request.user.save(update_fields=['friends_count'])

        other_user.friends_count = other_user.friends.count()
        other_user.save(update_fields=['friends_count'])

        return JsonResponse({'message': 'Friendship request accepted'})

    existing_request = FriendshipRequest.objects.filter(
        created_for=other_user,
        created_by=request.user,
        status=FriendshipRequest.SENT,
    ).first()

    if existing_request:
        return JsonResponse({'message': 'Request already sent'}, status=200)

    FriendshipRequest.objects.create(created_for=other_user, created_by=request.user)

    return JsonResponse({'message': 'Request sent'})


@api_view(['POST'])
def handle_request(request, pk, status):
    allowed_status = (FriendshipRequest.ACCEPTED, FriendshipRequest.REJECTED)

    if status not in allowed_status:
        return JsonResponse({'message': 'Invalid status provided.'}, status=400)

    other_user = get_object_or_404(User, pk=pk)
    friendship_request = FriendshipRequest.objects.filter(
        created_for=request.user,
        created_by=other_user,
        status=FriendshipRequest.SENT,
    ).first()

    if not friendship_request:
        return JsonResponse({'message': 'Friendship request not found.'}, status=404)

    friendship_request.status = status
    friendship_request.save(update_fields=['status'])

    if status == FriendshipRequest.ACCEPTED:
        request.user.friends.add(other_user)
        request.user.friends_count = request.user.friends.count()
        request.user.save(update_fields=['friends_count'])

        other_user.friends_count = other_user.friends.count()
        other_user.save(update_fields=['friends_count'])

    return JsonResponse({'message': 'Friendship updated'})
