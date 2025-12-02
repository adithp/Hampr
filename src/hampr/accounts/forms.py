from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from core.validaters import validate_indian_phone_number


class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ['first_name','last_name','email','username','password1','password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'First Name','required':False}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light', 'placeholder': 'example@email.com'}),
            
        }
    
  
class EmailOrUsernameLogin():
    username = forms.CharField(label="Username or password")