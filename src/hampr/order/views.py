from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from order.models import Order,OrderAddress
from accounts.models import UserAddress
from coupons.models import PromoCode

# Create your views here.

# <QueryDict: {'csrfmiddlewaretoken': ['E8v4DDDLYYS2S8jbnuEfi1BJWqew5XEECk0BBdNwvAIjjfyxTZsymx2jXNWuB3Os'], 'deliveryAddress': ['dceaba52-39d1-4a86-b0fd-1fdffcf5d5ba'], 'paymentMethod': ['COD'], 'gift_message': ['ttttt'], 'promo': ['']}>

class CreateOrderView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        data = request.POST
        user = request.cart
        if hasattr(user,'current_cart'):
                cart = user.current_cart
                grand_total = cart.get_grand_total()
                products_total = cart.get_products_total()
                decorations_total = cart.get_decoration_total()
                discount_amount = 0
                work_pomo = None
                subtotal=cart.get_grand_total()
        else:
            #return the error message
            return False
        if data.get('deliveryAddress',''):
            try:
                address_id = data.get('deliveryAddress','')
                address_obj = UserAddress.objects.get(id=address_id)
                
            except UserAddress.DoesNotExist as e:
                print(e)
            if data.get('paymentMethod') == 'COD':
                address = OrderAddress.objects.create(
                    address_type=address_obj.address_type,
                    city=address_obj.city,
                    country=address_obj.country,
                    landmark=address_obj.landmark,
                    phone_number=address_obj.phone_number,
                    secondary_phone_number=address_obj.secondary_phone_number,
                    postal_code=address_obj.postal_code,
                    recipient_name=address_obj.recipient_name,
                    street_address=address_obj.street_address,
                    apartment=address_obj.apartment,
                    state=address_obj.state,
                    user=request.user
                )
                if data.get('promo',''):
                    promo = data.get('promo')
                    if promo:
                        promo_obj = PromoCode.custom_objects().filter(code=promo).first()
                        if promo_obj:
                            if promo_obj.valid_token:
                                grand_total = cart.get_grand_total()
                                if  promo_obj.minimum_order_amount <= grand_total:
                                    if promo_obj.discount_type == 'PERCENT':
                                        discount_amount = (promo_obj.discount_value / 100) * grand_total
                                        if discount_amount > promo_obj.maximum_discount:
                                            discount_amount = promo_obj.maximum_discount
                                        grand_total = grand_total-discount_amount
                                        work_pomo = promo_obj
                                    elif promo_obj.discount_type == 'AMOUNT':
                                        if not grand_total < promo_obj.discount_value: 
                                            grand_total = grand_total-promo_obj.discount_value
                                            discount_amount = promo_obj.discount_value 
                                            work_pomo = promo_obj
                    
            
                
                                              
                                        

                
                order_obj = Order(user=request.user,delivery_address=address,gift_message=data.get('gift_message',''),promo_code=work_pomo if work_pomo else None,box_price=cart.box_size.price,products_total =products_total,decorations_total=decorations_total,subtotal=subtotal,discount=discount_amount,total_amount=grand_total,payment_method='COD',is_cod=True)
                order_obj.save()
                
        else:
            print('must add delivery address')