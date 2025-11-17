# Import Depnendencies
from django.shortcuts import render
from django.http import HttpResponse

# Import Components
from .models import User

# Create your views here.
def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()

        return HttpResponse('User activated. Try logging in with your Credentials.')
    else:
        return HttpResponse('Invalid activation link.')