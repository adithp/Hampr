import requests
from django.conf import settings



def get_shiprocket_token():
    response = requests.post(
        "https://apiv2.shiprocket.in/v1/external/auth/login",
        json={
            "email": settings.SHIPROCKET_EMAIL,
            "password": settings.SHIPROCKET_PASSWORD
        },
        timeout=5
    )

    data = response.json()
    return data.get("token")

def check_serviceability(delivery_pincode,pickup_pincode='673542', weight=None):
    token = get_shiprocket_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "pickup_postcode": pickup_pincode,
        "delivery_postcode": delivery_pincode,
        "weight": weight or 0.5,   # fallback weight
        "cod": 0
    }

    response = requests.get(
        "https://apiv2.shiprocket.in/v1/external/courier/serviceability/",
        headers=headers,
        params=params,
        timeout=5
    )

    data = response.json()
    couriers = data.get("data", {}).get("available_courier_companies", [])

    if not couriers:
        return False, None

    best = couriers[0]
    return True, best.get("estimated_delivery_days")


def build_shiprocket_items(order):
    
    
    return[{
        'name':order.
    }]



