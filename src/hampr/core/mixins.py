from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache



class NeverCacheMixin:

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    