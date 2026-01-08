from django.urls import path

from .views import CheckPromoCode

app_name = 'promo'

urlpatterns = [
    path('check_promo_code/',CheckPromoCode.as_view(),name='check_promo_code')
]
