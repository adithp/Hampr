from datetime import datetime
from order.models import OrderAddress
from django.contrib import messages
from django.shortcuts import redirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import localtime

from .order_email_config import ORDER_EMAIL_CONFIG


from .models import OrderItem,OrderDecoration,OrderHamper
from coupons.models import PromoCode
from .exceptions import insufficientStockException


def generate_order_number(order_id):
    date_str = datetime.now().strftime("%Y%m%d")
    return f"HMP-{date_str}-{order_id:04d}"



def create_order_address(address_obj,user):
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
            user=user
                    )
    return address

def promo_apply_validation(request,cart,promo):
    
    promo_obj = PromoCode.custom_objects().filter(code=promo).first()

    if not promo_obj:
        messages.error(request, "Invalid promo code.")
        return redirect('checkout:checkout_page')

    if not promo_obj.valid_token:
        messages.error(request, "This promo code is expired or inactive.")
        return redirect('checkout:checkout_page')

    grand_total = cart.get_grand_total()

    if promo_obj.minimum_order_amount > grand_total:
        messages.error(
            request,
            f"Minimum order amount ₹{promo_obj.minimum_order_amount} required for this promo code."
        )
        return redirect('checkout:checkout_page')

    
    if promo_obj.discount_type == 'PERCENT':
        discount_amount = (promo_obj.discount_value / 100) * grand_total
        if discount_amount > promo_obj.maximum_discount:
            discount_amount = promo_obj.maximum_discount
        grand_total -= discount_amount
        work_pomo = promo_obj

    elif promo_obj.discount_type == 'AMOUNT':
        if grand_total < promo_obj.discount_value:
            messages.error(request, "Promo discount exceeds order amount.")
            return redirect('checkout:checkout_page')

        discount_amount = promo_obj.discount_value
        grand_total -= discount_amount
        work_pomo = promo_obj

    return grand_total, discount_amount, promo_obj



def create_order_items(cart,order_obj):
    products = cart.cart_products.all()
    decorations = cart.cart_decoartion.all()
    for product in products:
        image = product.product_varient.variants_images.filter(is_thumbnail=True).first().image
        if not image:
            image = product.product_varient.variants_images.all().first().image
        if product.product_varient.stock < product.quantity:
            if product.product_varient.stock == 0:
                raise insufficientStockException(f"{product.product_varient.product.name} out of stock")
            else:
                raise insufficientStockException(f"{product.product_varient.product.name} only stock available {product.product_varient.stock}")
            
        OrderItem.objects.create(
            order=order_obj,
            product =product.product_varient,
            product_name=product.product_varient.product.name,
            product_brand=product.product_varient.product.brand,
            color_name =product.product_varient.color.name if product.product_varient.color else None,
            size_name =product.product_varient.size.name if product.product_varient.size else None,
            height=product.product_varient.height,
            width=product.product_varient.width,
            depth=product.product_varient.depth,
            price_at_order_time=product.product_varient.price,
            quantity=product.quantity,
            subtotal=product.product_varient.price * product.quantity,
            product_image=image
        )
        product.product_varient.stock -= product.quantity
        product.product_varient.save()
    for decoration in decorations:
        image = decoration.decoration.decoartion_image.filter(is_thumbnail=True).first().image
        if not image:
            image = decoration.decoration.decoartion_image.all().first().image
        if decoration.decoration.stock < decoration.quantity:
            if decoration.decoration.stock == 0:
                raise insufficientStockException(f"{decoration.decoration.name} out of stock")
            else:
                raise insufficientStockException(f"{decoration.decoration.name} only stock available {decoration.decoration.stock}")
        OrderDecoration.objects.create(
            order=order_obj,
            decoration=decoration.decoration,
            decoration_name=decoration.decoration.name,
            height=decoration.decoration.height,
            width=decoration.decoration.width,
            depth=decoration.decoration.depth,
            is_inside=False if decoration.position == 'outer' else True,
            is_outside=True if decoration.position == 'outer' else False,
            price_at_order_time=decoration.decoration.price,
            quantity=decoration.quantity,
            subtotal=decoration.quantity * decoration.decoration.price,
            image=image
        )
        decoration.decoration.stock -= decoration.quantity
        decoration.decoration.save()
        
    if cart.box_size.stock == 0:
         raise insufficientStockException(f"{cart.box_size.box.name} out of stock")
    cart.box_size.stock -= 1
    cart.box_size.save()
    box_image = cart.box.box_images.filter(is_thumbnail=True).first().image
    if not box_image:
        box_image = cart.box.box_images.all().first().image
    OrderHamper.objects.create(
        order=order_obj,
        hamper=cart.box_size,
        hamper_name=cart.box.name,
        category_name=cart.box.category.name,
        size_label=cart.box_size.size_label,
        height=cart.box_size.height,
        width=cart.box_size.width,
        depth=cart.box_size.depth,
        box_price_at_order_time = cart.box_size.price,
        box_image=box_image
    )
    
        

    


def send_order_email(user, order, email_type, extra_context=None):
    try:
        print("Email Sending Started")
        config = ORDER_EMAIL_CONFIG.get(email_type)
        if not config:
            return

        context = {
            "customer_name": user.first_name or "Customer",
            "email_message": config["message"],
            "order_id": order.order_number,
            "order_date": order.created_at.strftime("%d %b %Y"),
            "order_status": config["status"],
            "total_amount": order.total_amount,
            "order_url": f"https://yourwebsite.com/orders/{order.id}/",
        }

        if extra_context:
            context.update(extra_context)

        html_content = render_to_string("order/order-email.html", context)

        email = EmailMultiAlternatives(
            subject=config["subject"],
            body=config["status"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
        print("✅ After email.send()")
    except Exception as e:
        print(e)

