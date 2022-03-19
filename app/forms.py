from django import forms
from django_registration.forms import RegistrationForm

from .models import User


class MyCustomUserForm(RegistrationForm):
    class Meta:
        model = User
        fields = ('username','email', 'full_name')