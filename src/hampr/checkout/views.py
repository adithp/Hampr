from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from accounts.models import UserAddress,CustomUser

from core.mixins import OnlyForUsers
from courier.services import check_serviceability


class CheckoutPageView(LoginRequiredMixin,OnlyForUsers,View):
    def get(self,request,*args, **kwargs):
        address = UserAddress.objects.filter(user=request.user)
        for item in address:
            result = check_serviceability(delivery_pincode=item.postal_code)
            print(result[0])
            item.available = result[0]
            item.expected_data = result[1]
            
        print(address)
        if CustomUser.objects.filter(id=request.user.id).exists():
            user = CustomUser.objects.get(id=request.user.id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                products = cart.cart_products.all()
                decoration = cart.cart_decoartion.all()
                
                for i in products:
                    i.total_paroduct = i.product_varient.price * i.quantity
            else:
                return HttpResponse("First Add Products To Cart")
        print(address[0].available)
        return render(request,'checkout/checkout.html',{'address':address,'cart':cart,'products':products,'decoration':decoration})
    def post(self,request,*args, **kwargs):
        print(request.POST)
        return render(request,'order/order-placed.html')


