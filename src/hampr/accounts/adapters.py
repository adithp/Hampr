from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse
from django.urls import reverse



class GoogleBlockAdapter(DefaultSocialAccountAdapter):
     def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return  
        if user.has_usable_password():
            messages.error(request, "You already registered using email & password. Please login using your password.")
            raise ImmediateHttpResponse(
                redirect(reverse("accounts:login"))
            )
        
       
        return