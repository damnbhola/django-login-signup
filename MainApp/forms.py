from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100, required=True)
    address = forms.Textarea()
    phone_number = forms.CharField(max_length=12, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'address',
            'phone_number'
        ]
