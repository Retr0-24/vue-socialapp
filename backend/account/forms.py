# Import Dependencies
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Import Components
from .models import User

# Handle Validation
class signUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2',]
      
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'avatar']