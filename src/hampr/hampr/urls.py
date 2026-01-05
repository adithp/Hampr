
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('accounts.urls')),
    path('custom_admin/',include('admin_panel.urls')),
    path('accounts/', include('allauth.urls')),
    path('',include('core.urls')),
    path('shop/', include('catalog.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('cart/',include('cart.urls')),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

