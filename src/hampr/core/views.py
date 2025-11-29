from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

from django.views.generic import TemplateView


class CommonLogoutView(View):
    
    def get(self,request,*args, **kwargs):
        user = request.user
        logout(request)
        
        if user.is_superuser or user.is_staff:
            return redirect('cadmin:admin_login')
        else:
            return redirect('accounts:login')
        
        
class LandingPageRenderView(TemplateView):
    template_name = 'core/landing.html'
    

    