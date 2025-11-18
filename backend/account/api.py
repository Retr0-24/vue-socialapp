# Import Depnendencies
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

# Import Components
from .forms import signUpForm, ProfileForm
from .models import FriendshipRequest
from .models import User
from .serializers import UserSerializer, FriendshipRequestSerializer
from notification.utils import create_notification


# Create your views here.

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'email': request.user.email,
        'name': request.user.name,
        'avatar': request.user.get_avatar(),
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
        user = form.save()
        user.is_active = False
        user.save()

        url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'

        send_mail(
            "Please Verify Email",
            f"Your Account is not activated please click this Link you Verirfy your Account: {url}",
            "noreply@socialapp.com",
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors.as_json()

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

@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email is already in use.'}, status=400)

    else:
        form = ProfileForm(request.POST or None, request.FILES or None, instance=user)

        if form.is_valid():
            form.save()

            serializer = UserSerializer(user)
            
            return JsonResponse({
                'message': 'Profile updated',
                'user': UserSerializer(user).data
            })

        return JsonResponse({'message': 'Invalid data submitted.'}, status=400)


@api_view (['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'Success'})  
    else:
        return JsonResponse({'message': form.errors.as_json()})


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

    friendrequest = FriendshipRequest.objects.create(created_for=other_user, created_by=request.user)

    notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)

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

        notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'Friendship updated'})
