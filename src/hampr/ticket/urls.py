from django.urls import path
from .views import ContactView

app_name = 'ticket'

urlpatterns = [
    path('connect/',ContactView.as_view(),name='contact'),
    
]
