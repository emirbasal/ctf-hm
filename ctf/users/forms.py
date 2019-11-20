from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='This email is only used for academic purposes')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')