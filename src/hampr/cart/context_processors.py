from accounts.models import CustomUser

def cart_items_count(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        if hasattr(user,'current_cart'):
            cart =user.current_cart
            count = 1
            count += cart.cart_products.all().count()
            count += cart.cart_decoartion.all().count()
            return {'total_type_items_count':count}
    return {}