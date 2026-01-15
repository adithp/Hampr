import requests
from django.conf import settings
import shippo
import json





shippo.set_api_key = settings.SHIPPO_API_KEY

def check_serviceability(delivery_pincode, pickup_pincode="673542", weight=1):
    try:
        # 1. Define the Endpoint
        url = "https://api.goshippo.com/shipments/"

        # 2. Set Headers (This is the critical part for Auth)
        headers = {
            "Authorization": f"ShippoToken {settings.SHIPPO_API_KEY}",
            "Content-Type": "application/json"
        }

        # 3. Define the Payload (The Data)
        payload = {
           "address_from": {
                "name": "Shippo Test HQ",
                "street1": "215 Clayton St.",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94117",
                "country": "US"
            },
            "address_to": {
                "name": "Recipient",
                "street1": "Test St",
                "city": "Test City",
                "zip": str(delivery_pincode),
                "country": "IN"
            },
            "parcels": [{
                "length": "5", "width": "5", "height": "5",
                "distance_unit": "in", "weight": "1", "mass_unit": "lb"
            }],
            "async": False
        }

        # 4. Make the Request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        print(data)

        # 5. Check for Rates
        if response.status_code == 201 and data.get('rates'):
            print(f"✅ Serviceable! Found {len(data['rates'])} carriers.")
            return True
        else:
            print("❌ Not Serviceable or Error.")
            # Print the error message from Shippo to help debugging
            if 'rates' not in data:
                print(f"Shippo Response: {data}")
            return False

    except Exception as e:
        print(f"API CONNECTION ERROR: {e}")
        return False

  
def build_shiprocket_items(order):

    return[{
        'name':'Custom Hamper Box',
        "sku":f"HAMPER-{order.order_number}",
        "units":1,
        "selling_price":float(order.total_amount)
    }]



