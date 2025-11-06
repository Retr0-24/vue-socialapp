# Import Depnendencies
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse

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
        requests = FriendshipRequest.objects.filter(created_for=request.user)
    
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user),
        'friends': UserSerializer(friends, many=True),
        'requests': FriendshipRequestSerializer(requests, many=True)
    }, safe=False)

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    friendship_request = FriendshipRequest(created_for=user, created_by=request.user)

    return JsonResponse({'message': 'Request Send'})