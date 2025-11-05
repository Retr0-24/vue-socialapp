# Import Depnendencies
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import signUpForm

# Import Django Components
from django.http import JsonResponse


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