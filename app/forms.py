from django import forms
from django_registration.forms import RegistrationForm

from .models import Post, User


class MyCustomUserForm(RegistrationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'bio', 'neighbourhood', 'location', 'contact')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
