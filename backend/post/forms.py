# Import Dependencies
from django.forms import ModelForm

# Import Components
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
