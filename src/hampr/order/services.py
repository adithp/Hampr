from datetime import datetime
from order.models import OrderAddress
from courier.services import build_shiprocket_items
import requests




from .models import OrderItem,OrderDecoration,OrderHamper






def generate_order_number(order_id):
    date_str = datetime.now().strftime("%Y%m%d")
    return f"HMP-{date_str}-{order_id:04d}"


def check_serviceability_with_cod(token, pickup_pincode, delivery_pincode, is_cod):
    url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "pickup_postcode": pickup_pincode,
        "delivery_postcode": delivery_pincode,
        "cod": 1 if is_cod else 0,
        "weight": 1.0
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    result = response.json()
    data = result.get("data", {})
    couriers = data.get("available_courier_companies", [])

   
    if not couriers:
        return False, None

    recommended_id = data.get("recommended_courier_company_id")

    
    courier = next(
        (c for c in couriers if c.get("courier_company_id") == recommended_id),
        couriers[0]
    )

    eta_days = int(courier.get("estimated_delivery_days", 0))

    return True, eta_days




def create_order_address(user_address,user):
    order_address = OrderAddress.objects.create(
        address_type=user_address.address_type,
        city=user_address.city,
        country=user_address.country,
        landmark=user_address.landmark,
        phone_number=user_address.phone_number,
        secondary_phone_number=user_address.secondary_phone_number,
        postal_code=user_address.postal_code,
        recipient_name=user_address.recipient_name,
        street_address=user_address.street_address,
        apartment=user_address.apartment,
        state=user_address.state,
        user=user,
    )
    return order_address


def build_shiprocket_payload(order,address,cart):
    
    return {
        "order_id": order.order_number,
        "order_date": order.created_at.strftime("%Y-%m-%d"),
        "pickup_location": "warehouse",
        "billing_customer_name": address.recipient_name,
        "billing_address": address.street_address,
        "billing_city": address.city,
        "billing_pincode": address.postal_code,
        "billing_state": address.state,
        "billing_country": "India",
        "billing_phone": address.phone_number,
        "billing_email": order.user.email,
        
        "shipping_is_billing": True,
        "order_items": build_shiprocket_items(order),
        
        "payment_method": "COD" if order.is_cod else "Prepaid",
        "sub_total": float(order.total_amount),
        
        "length": float(cart.box_size.width),
        "breadth":  float(cart.box_size.depth),
        "height": float(cart.box_size.height),
        "weight": 1.0,
        
    }
    
    


SHIPROCKET_CREATE_ORDER_URL = (
    "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
)

def create_shiprocket_order(token, payload):
   
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        SHIPROCKET_CREATE_ORDER_URL,
        json=payload,
        headers=headers,
        timeout=30
    )
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)  

   
    # response.raise_for_status()

    return response.json()


def create_order_items(cart,order_obj):
    products = cart.cart_products.all()
    decorations = cart.cart_decoartion.all()
    for product in products:
        image = product.product_varient.variants_images.filter(is_thumbnail=True).first().image
        if not image:
            image = product.product_varient.variants_images.all().first().image

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
    for decoration in decorations:
        image = decoration.decoration.decoartion_image.filter(is_thumbnail=True).first().image
        if not image:
            image = decoration.decoration.decoartion_image.all().first().image
        
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
    
        
    
        
    