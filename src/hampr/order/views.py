from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from datetime import timedelta
from django.db import transaction
from django.utils import timezone


from order.models import Order,OrderAddress
from accounts.models import UserAddress
from coupons.models import PromoCode
from .services import generate_order_number,create_order_address,build_shiprocket_payload,check_serviceability_with_cod,create_shiprocket_order,create_order_items


# Create your views here.

# <QueryDict: {'csrfmiddlewaretoken': ['E8v4DDDLYYS2S8jbnuEfi1BJWqew5XEECk0BBdNwvAIjjfyxTZsymx2jXNWuB3Os'], 'deliveryAddress': ['dceaba52-39d1-4a86-b0fd-1fdffcf5d5ba'], 'paymentMethod': ['COD'], 'gift_message': ['ttttt'], 'promo': ['']}>

class CreateOrderView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        data = request.POST
        user = request.user
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
                with transaction.atomic():
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
                    order_no = generate_order_number(order_obj.id)
                    order_obj.order_number = order_no
                    order_obj.save()
                    # token = get_shiprocket_token()
                    is_serviceable, eta_days  = check_serviceability_with_cod(token,'673328',address.postal_code,order_obj.is_cod)
                    print(is_serviceable,eta_days)
                    if not is_serviceable:
                        return HttpResponse("Address Not Deliverable")
                    if eta_days:
                        order_obj.expected_delivery = timezone.now() + timedelta(days=eta_days)
                        order_obj.save(update_fields=["expected_delivery"])
                    create_order_items(cart,order_obj)
                    payload = build_shiprocket_payload(order_obj,address,cart)
                    # token = get_shiprocket_token()
                    result = create_shiprocket_order(token, payload)
                    order_obj.shipment_id = result.get("shipment_id")
                    order_obj.save(update_fields=["shipment_id"])
                    cart.delete()
                
                
                
        else:
            print('must add delivery address')