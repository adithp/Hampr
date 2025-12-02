from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect


class NeverCacheMixin:

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        print('Never Cache mixixn is worked')
        return super().dispatch(request, *args, **kwargs)
    
    
    
class GuestOnlyMixin:
    redirect_url = 'core:landing_page'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)