from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


    
def otp_pending_verify(func):
    @wraps(func)
    def wrapper(request,*args, **kwargs):
        if 'otp_pending' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('accounts:signup')
    return wrapper

def guest_only(func):
    @wraps(func)
    def wrapper(request,*args, **kwargs):
        user = request.user
        if  user.is_authenticated:
            return redirect('accounts:suc')
        return func(request,*args, **kwargs)
    return wrapper
        