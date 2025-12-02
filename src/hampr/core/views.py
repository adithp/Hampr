from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .mixins import NeverCacheMixin
from django.views.generic import TemplateView
from django.contrib import messages
from accounts.models import CustomUser



class CommonLogoutView(View):
    
    def post(self,request,*args, **kwargs):
        user = request.user
        logout(request)
        print(request.user)
        list(messages.get_messages(request)) 
        return redirect('core:landing_page_redirect',user.id)
        
        
class LandingPageRenderView(NeverCacheMixin,TemplateView):
    template_name = 'core/landing.html'
    
    
def after_logout(request,user_id):
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except:
        print("Error Happend")

    if user.is_superuser or user.is_staff:
            return redirect('cadmin:admin_login')
    else:
        return redirect('accounts:login')



   

    