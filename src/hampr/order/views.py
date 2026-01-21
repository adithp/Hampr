# from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import uuid
from django.db import transaction
from django.shortcuts import redirect,render
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import json


from order.models import Order
from accounts.models import UserAddress
from coupons.models import PromoCode,PromoCodeUsage
from courier.services import check_serviceability
from .services import generate_order_number,create_order_items,create_order_address,promo_apply_validation
from payment.razorpay_client import create_razorpay_order
from payment.models import Payment,PaymentGatewayLog
from core.utils import invoice_generator
from reviews.models import ProductReviews,DecorationReviews,BoxReviews


# Create your views here.

# <QueryDict: {'csrfmiddlewaretoken': ['E8v4DDDLYYS2S8jbnuEfi1BJWqew5XEECk0BBdNwvAIjjfyxTZsymx2jXNWuB3Os'], 'deliveryAddress': ['dceaba52-39d1-4a86-b0fd-1fdffcf5d5ba'], 'paymentMethod': ['COD'], 'gift_message': ['ttttt'], 'promo': ['']}>

class CreateOrderView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        order_obj = None
        data = request.POST
        print(data)
        user = request.user
        if hasattr(user,'current_cart'):
                cart = user.current_cart
                grand_total = cart.get_grand_total()
                products_total = cart.get_products_total()
                decorations_total = cart.get_decoration_total()
                discount_amount = 0
                work_promo = None
                subtotal=cart.get_grand_total()
        else:
            #return the error message
            return False
        if data.get('deliveryAddress',''):
            try:
                address_id = data.get('deliveryAddress','')
                address_obj = UserAddress.objects.get(id=address_id, user=request.user)
        
                
            except UserAddress.DoesNotExist as e:
                print(e)
            is_serviceable = check_serviceability(address_obj.postal_code)
            if not is_serviceable:
                messages.error(request, "Address is not deliverable.")
                return redirect('checkout:checkout_page')

            if data.get('paymentMethod') == 'COD':
                with transaction.atomic():
                    address = create_order_address(address_obj,request.user)
                    if data.get('promo', ''):
                        result = promo_apply_validation(request,cart,data.get('promo',''))
                        if not isinstance(result,tuple):
                            return result
                        grand_total, discount_amount, work_promo = result
                    order_obj = Order(user=request.user,delivery_address=address,gift_message=data.get('gift_message',''),promo_code=work_promo if work_promo else None,box_price=cart.box_size.price,products_total =products_total,decorations_total=decorations_total,subtotal=subtotal,discount=discount_amount,total_amount=grand_total,payment_method='COD',is_cod=True,)
                    order_obj.save()
                    order_no = generate_order_number(order_obj.id)
                    order_obj.order_number = order_no
                    order_obj.save()
            elif data.get('paymentMethod') == 'ONLINE':
                with transaction.atomic():
                    address = create_order_address(address_obj,request.user)
                    if data.get('promo', ''):
                        result = promo_apply_validation(request,cart,data.get('promo',''))
                        if not isinstance(result,tuple):
                            return result
                        grand_total, discount_amount, work_promo = result
                    order_obj = Order(user=request.user,delivery_address=address,gift_message=data.get('gift_message',''),promo_code=work_promo if work_promo else None,box_price=cart.box_size.price,products_total =products_total,decorations_total=decorations_total,subtotal=subtotal,discount=discount_amount,total_amount=grand_total,payment_method='ONLINE',is_cod=False,)
                    order_obj.save()
                    order_no = generate_order_number(order_obj.id)
                    order_obj.order_number = order_no
                    order_obj.save()
                    payment = Payment.objects.create(
                        user=user,
                        order=order_obj,
                        amount=order_obj.total_amount,
                        payment_method="RAZORPAY",
                        transaction_id=f"INIT-{uuid.uuid4()}",
                        status="PENDING"
                    )

                    rp_order = create_razorpay_order(payment.amount)

                    payment.gateway_response_id = rp_order["id"]
                    payment.save()

                
                    PaymentGatewayLog.objects.create(
                        payment=payment,
                        gateway_name="RAZORPAY",
                        request_data={"amount": str(payment.amount)},
                        response_data=rp_order,
                        status_code="ORDER_CREATED"
                    )
            if order_obj.is_cod == True:
                create_order_items(cart,order_obj)
                cart.delete()
                order_obj.status = "CONFIRMED"
                if order_obj.promo_code:
                    promousage_obj =PromoCodeUsage(discount_given=discount_amount,promo_code=work_promo,user=request.user,order=order_obj)
                    promousage_obj.save()
                    work_promo.used_count = work_promo.used_count + 1
                    work_promo.save()
                order_obj.save()
                return redirect('order:order_succsess',order_id=order_obj.order_number)
            elif order_obj.is_cod == False:
                return JsonResponse({
                            "payment_type": "RAZORPAY",
                            "order_id": rp_order["id"],
                            "amount": rp_order["amount"],
                            "key": settings.RAZORPAY_KEY_ID
                        })
                
                
        else:
            print('must add delivery address')
            
            
class OrderSuccsessView(LoginRequiredMixin,View):
    def get(self,request,order_id,*args, **kwargs):
        user = request.user 
        try:
            order = Order.objects.get(user=user,order_number=order_id,status='CONFIRMED')
        except Order.DoesNotExist as e:
            print(e)
            return redirect('core:landing_page')
        return render(request,'order/order-placed.html',{'order_id':order.order_number})
        
    
    
    


def razorpay_verify(request):
    data = json.loads(request.body)

    payment = Payment.objects.get(
        gateway_response_id=data["razorpay_order_id"]
    )

    # mark payment success
    payment.transaction_id = data["razorpay_payment_id"]
    payment.status = "SUCCESS"
    payment.save()

    order = payment.order
    if order.promo_code:
        PromoCodeUsage.objects.create(
            discount_given=order.discount,
            promo_code=order.promo_code,
            user=order.user,
            order=order
        )
        order.promo_code.used_count += 1
        order.promo_code.save()
    create_order_items(order.user.current_cart, order)
    order.user.current_cart.delete()

    order.status = "CONFIRMED"
    order.save()
    

    return JsonResponse({
        "status": "success",
        "order_number": order.order_number
    })
    
    
class OrderDetail(LoginRequiredMixin,View):
    def get(self,request,order_id,*args, **kwargs):
        try:
            order = Order.objects.get(order_number=order_id)
        except Order.DoesNotExist as e:
            print(e)
             

        order_items = list(order.items.all())
        order_hampers = list(order.order_hampers.all())
        order_decorations = list(order.order_decorations.all())

        product_reviews = ProductReviews.objects.filter(
            user=request.user,
            product__in=[item.product.product for item in order_items]
        )
        product_review_map = {r.product_id: r for r in product_reviews}

        box_reviews = BoxReviews.objects.filter(
            user=request.user,
            box__in=[h.hamper.hamper_box for h in order_hampers]
        )
        box_review_map = {r.box_id: r for r in box_reviews}

        decoration_reviews = DecorationReviews.objects.filter(
            user=request.user,
            decoration__in=[d.decoration for d in order_decorations]
        )
        decoration_review_map = {r.decoration_id: r for r in decoration_reviews}

        for item in order_items:
            item.user_review = product_review_map.get(item.product.product.id)

        for hamper in order_hampers:
            hamper.user_review = box_review_map.get(hamper.hamper.hamper_box.id)

        for decoration in order_decorations:
            decoration.user_review = decoration_review_map.get(decoration.decoration.id)

        invoice = request.GET.get('invoice')
        if invoice == "true":
            return invoice_generator(order)

        context = {
            'order': order,
            'order_items': order_items,           
            'order_hampers': order_hampers,
            'order_decorations': order_decorations,
        }
        return render(request, 'order/order-detail.html', context)