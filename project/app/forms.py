# app/forms.py

from django import forms
from .models import Blog,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# app/forms.py
from django import forms

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content'] 
 # Specify which fields from the Blog model should be included in the form

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']
