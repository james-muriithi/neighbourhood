from django import forms
from django_registration.forms import RegistrationForm

from .models import Business, Post, User


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


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'description', 'email', 'image')


class UpdateBusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'description', 'email')


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
