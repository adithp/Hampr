from django.urls import path

from .views import check_availability


app_name = 'courier'

urlpatterns = [
    path('check_pincode/',check_availability,name='pincode_check')
]