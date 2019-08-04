from django import forms
from .models import *

class postForm(forms.ModelForm):
    class meta:
        model = Post
        exclude = [""]