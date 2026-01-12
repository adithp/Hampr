from django.shortcuts import render
from courier.services import check_serviceability
from django.http import JsonResponse
# Create your views here.


def check_availability(request):
    pincode = request.GET.get('pincode')
    result  = check_serviceability(delivery_pincode=pincode)
    return JsonResponse({
            "success": result[0],
            "days": result[1],
    })
    
