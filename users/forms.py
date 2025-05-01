from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass
