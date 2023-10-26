from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Confirm password'}))

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']
