from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from core.validaters import validate_indian_phone_number


class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ['first_name','last_name','email','username','password1','password2']
        widgets = {
            'first_name':forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Jhon',
                
            }),
            'last_name':forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Doe',
                
            }),
            'email':forms.EmailInput(attrs={
                'type':'email',
                'placeholder':'example@email.com',
                'required':True
                
            }),
            'username':forms.TextInput(attrs={
                'type':'text',
                'placeholder':'jhondoe',
                'required':True
                
            }),
            'password1':forms.PasswordInput(attrs={
                'type':'password',
                'placeholder':'••••••••',
                'required':True
            })
            ,
            'password2':forms.PasswordInput(attrs={
                'type':'password',
                'placeholder':'••••••••',
                'required':True
            })
            
        }
    
  
class EmailOrUsernameLogin():
    username = forms.CharField(label="Username or password")