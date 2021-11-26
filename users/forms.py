from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import Profile, Report


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# This is for updating the username and password
class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(render_value=False)
        
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# This is for updating the profile fields and picture
class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['height'].label = "Height (in inches)"
        self.fields['dob'].label = "Date of Birth"
    
    class Meta:
        model = Profile
        fields = ['image','height', 'dob','sports',]


class UserReportForm(forms.ModelForm):
    """
    Form users can use to submit user reports to be reviewed by admins
    """

    # Set form model and fields
    class Meta:
        model = Report
        fields = ['message']