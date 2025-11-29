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
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,'user already register login with email and password')
            raise ImmediateHttpResponse(
                redirect(reverse("accounts:login"))
            )
        