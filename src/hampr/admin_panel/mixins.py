from django.shortcuts import redirect



class StaffRequiredMixin:
    redirect_url = 'cadmin:admin_login'
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(self.redirect_url) 
        return super().dispatch(request, *args, **kwargs)
    
    
class LoginInRedirectMixin:
    
    redirect_url = 'cadmin:admin_dashboard'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
    
    

    
    