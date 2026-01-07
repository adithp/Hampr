from django.urls import path

from .views import CheckoutPageView

app_name = 'checkout'

urlpatterns = [
    path('checkout-page/',CheckoutPageView.as_view(),name='checkout_page')
]