# Import Dependencies
from .models import User

# Import Django Components
from django.contrib.auth.forms import UserCreationForm

# Handle Validation
class signUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2']