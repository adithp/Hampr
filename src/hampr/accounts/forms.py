from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import UserAddress

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
    
    

class UserAddressForm(forms.ModelForm):
    
    

    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Enter a valid phone number (10–15 digits)."
            )
        ]
    )

    secondary_phone_number = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Enter a valid secondary phone number."
            )
        ]
    )

    class Meta:
        model = UserAddress
        fields = [
            "address_type",
            "recipient_name",
            "phone_number",
            "secondary_phone_number",
            "street_address",
            "apartment",
            "landmark",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]

        widgets = {
            "address_type": forms.RadioSelect(),
            "street_address": forms.Textarea(attrs={"rows": 2}),
            "landmark": forms.TextInput(attrs={"placeholder": "Optional"}),
            "recipient_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
        }

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")

        if len(str(postal_code)) != 6:
            raise ValidationError("Postal code must be exactly 6 digits.")

        return postal_code
    def clean_is_default(self):
        is_default = self.cleaned_data.get("is_default")
        print(is_default)
        
        if is_default and self.usert:
            existing_default = UserAddress.objects.filter(
                user=self.usert,
                is_default=True
            ).exclude(id=self.instance.id)
            print(existing_default)
            if existing_default.exists():
                raise ValidationError(
                    "You already have a default address."
                )

        return is_default

