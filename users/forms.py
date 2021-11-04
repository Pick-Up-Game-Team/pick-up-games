from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    Class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# This is for updating the username and password
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# This is for updating the profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        field = ['image']
