from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from accounts.models import UserAddress,CustomUser

from core.mixins import OnlyForUsers
# Create your views here.


class CheckoutPageView(LoginRequiredMixin,OnlyForUsers,View):
    def get(self,request,*args, **kwargs):
        address = UserAddress.objects.filter(user=request.user)
        print(address)
        if CustomUser.objects.filter(id=request.user.id).exists():
            user = CustomUser.objects.get(id=request.user.id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                products = cart.cart_products.all()
                decoration = cart.cart_decoartion.all()
        return render(request,'checkout/checkout.html',{'address':address,'cart':cart,'products':products,'decoration':decoration})


