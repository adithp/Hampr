from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from accounts.models import CustomUser
from django.db.models import Q
from django.contrib.auth import login
from django.db.models import Q

from .mixins import StaffRequiredMixin,LoginInRedirectMixin
from core.mixins import NeverCacheMixin




class AdminLoginView(NeverCacheMixin,LoginInRedirectMixin,View):
     def get(self, request, *args, **kwargs):
        return render(request,'c_admin/admin_login.html')
    
     def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(Q(username=identifier)| Q(email=identifier))
        except CustomUser.DoesNotExist:
            messages.error(request,"Invalid Username")
            return redirect(reverse_lazy('cadmin:admin_login'))
        if not user.check_password(password):
            messages.error(request,"password invalid")
            return redirect(reverse_lazy('cadmin:admin_login'))
        if not user.is_active:
            messages.error(request,"Contact superadmin admin blocked by superadmin")
            return redirect(reverse_lazy('cadmin:admin_login'))
        
        if not user.is_staff:
            messages.error(request,"only admin can access")
            return redirect(reverse_lazy('cadmin:admin_login'))
        user.backend = 'django.contrib.auth.backends.ModelBackend'  
        login(request,user)
        return redirect('cadmin:admin_dashboard')


class AdminDashboardView(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_count = CustomUser.objects.filter(is_superuser=False,is_staff=False).count()
        active_users = CustomUser.objects.filter(is_superuser=False,is_staff=False,is_active=True).count()
        blocked_users =  CustomUser.objects.filter(is_superuser=False,is_staff=False,is_active=False).count()
        context['users_count'] = users_count
        context['active_users'] = active_users
        context['blocked_users'] = blocked_users
        
        return context
    

class AdminUserManagement(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/user_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.objects.filter(is_superuser=False,is_staff=False)
        query = self.request.GET.get('q',{})
        if query:
            users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))

        context['users_list'] = users
        
        return context
    
    
class AdminBlockUser(StaffRequiredMixin,View):
    
    def get(self,request,id,*args, **kwargs):
        try:
            user = CustomUser.objects.get(id=id)
        except:
            pass
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('cadmin:user_management')