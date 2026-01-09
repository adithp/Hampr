from django.shortcuts import render

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from coupons.models import PromoCode

from core.mixins import OnlyForUsers
# Create your views here.
# Create your views here.
from django.http import JsonResponse


class CheckPromoCode(LoginRequiredMixin,OnlyForUsers,View):
    def post(self,request,*args, **kwargs):
        code = request.POST.get('code') 
        if not code:
            return JsonResponse({
                "success": False,
                "message": "Please enter a promo code"
            })
        codeobj = PromoCode.custom_objects().filter(code=code).first()
        if not codeobj:
            return JsonResponse({
                "success": False,
                "message": "Invalid promo code"
            })
        if not codeobj.valid_token():
             return JsonResponse({
                "success": False,
                "message": "This promo code is expired or inactive"
            })
        user = request.user
        if hasattr(user,'current_cart'):
                cart = user.current_cart
                grand_total = cart.get_grand_total()
                if not codeobj.minimum_order_amount <= grand_total:
                    return JsonResponse({
                "success": False,
                "message": f"Minimum order amount is ₹{codeobj.minimum_order_amount}"
            })

                if codeobj.discount_type == 'PERCENT':
                    discount_amount = (codeobj.discount_value / 100) * grand_total
                    if discount_amount > codeobj.maximum_discount:
                        discount_amount = codeobj.maximum_discount
                    preview_total = grand_total-discount_amount
                    return JsonResponse({
                    "success": True,
                    "message": "Promo code applied successfully",
                    "discount": round(discount_amount, 2),
                    "grand_total": round(preview_total, 2),
                    "code": codeobj.code
            })
                if codeobj.discount_type == 'AMOUNT':
                    if grand_total < codeobj.discount_value:
                        return JsonResponse({
                    "success": False,
                    "message": "Promo value exceeds cart total"
                })
                preview_total = grand_total-discount_amount        
                return JsonResponse({
                "success": True,
                "message": "Promo code applied successfully",
                "discount": round(discount_amount, 2),
                "grand_total": round(preview_total, 2),
                "code": codeobj.code
            })
                    
        else:
            return JsonResponse({
                "success": False,
                "message": "No active cart found"
            })