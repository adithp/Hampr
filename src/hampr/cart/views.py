from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.generic import DeleteView
from django.urls import reverse_lazy


from .models import CustomHamper,CartProduct,CartDecoration
from accounts.models import CustomUser
from catalog.models import BoxSize,HamperBox,ProductVariant,Decoration
from catalog.utilts import voulme_calculater




class Select_Box_View(LoginRequiredMixin,View):
    def post(self,request,id,*args, **kwargs):
        user_id = request.user.id
    
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist as e:
            print(e)      
        if hasattr(user,'current_cart'):
            user.current_cart.delete()
        try:
            box_size = BoxSize.objects.get(id=id)
        except BoxSize.DoesNotExist as e:
            print(e)
        if box_size.stock == 0:
            messages.error(
                request,
                "Sorry! This box size is out of stock. Please choose another size."
            )
            return redirect('shop:box_detail',slug=box_size.hamper_box.slug)
        cart = CustomHamper(box=box_size.hamper_box,box_size=box_size,user=user,total_price=box_size.price)
        cart.save()
    
        
        return redirect('shop:product_list')
        

class Replace_Box_View(LoginRequiredMixin,View):
    def post(self,request,id,*args, **kwargs):
        user_id = request.user.id
    
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist as e:
            print(e)      
        
        if not hasattr(user,'current_cart'):
            pass
        
        cart = user.current_cart
        
        try:
            box_size = BoxSize.objects.get(id=id)
        except BoxSize.DoesNotExist as e:
            print(e)
            
        cart.box = box_size.hamper_box
        cart.box_size = box_size
        cart.save()
        
        return redirect('shop:product_list')
    
        
class UpdateCartView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')
        item_type = data.get("type") 
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        
        
        if not hasattr(user,'current_cart'):
            return JsonResponse({
                "success": False,
                "message":"First Select The Box Then Only You Can Select Products"
                }, status=400)
        cart = user.current_cart
        if item_type == 'product':
            print(product_id)
            try:
                product_varient = ProductVariant.objects.get(id=product_id)
            except ProductVariant.DoesNotExist as e:
                return JsonResponse({
                    "success": False,
                    "error": "Product not found"
                }, status=400)
            print(cart.get_used_volume() , voulme_calculater(product_varient.height,product_varient.width,product_varient.depth))
            
            cart_item,created = CartProduct.objects.get_or_create(cart=cart,product_varient=product_varient,defaults={"quantity":0})
            if cart_item.quantity > product_varient.stock:
                return JsonResponse({
                    "success": False,
                    "error": "Stock is out of range. Please update your cart."
                }, status=400)
            if action == "increment":
                if cart.get_used_volume() + voulme_calculater(product_varient.height,product_varient.width,product_varient.depth) > voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth):
                    if created:
                        cart_item.delete()
                    return JsonResponse({
                        "success": False,
                        "error": "Box is Out Of Range Box Maximum Excided."
                    }, status=400)
                if product_varient.stock > cart_item.quantity:
                    cart_item.quantity += 1
                else:
                    return JsonResponse({
                        "success": False,
                        "error": "Not enough stock available"
                    }, status=400)
                            
            elif action == 'decrement':
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    return JsonResponse({
                        "success": True,
                        "quantity": 0,
                        "cart": {
                        "products": cart.get_products_json(),
                        "products_total": float(cart.get_products_total()),
                        "grand_total": float(cart.get_grand_total()),
                        'used_volume':float(cart.get_used_volume()),
                        'volume':float(voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth))
                    }
                    })
                
        elif item_type == 'decoration':
            position = data.get("position")
            
            try:
                decoration = Decoration.objects.get(id=product_id)
                print(decoration.id,decoration.name,decoration.stock,decoration.width)
            except Decoration.DoesNotExist as e:
                 return JsonResponse({
                    "success": False,
                    "error": "Invalid decoration"
                }, status=400)
            if position not in ['inner', 'outer']:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid decoration position"
                }, status=400)
            if position == 'inner':
                if not decoration.is_inside:
                     return JsonResponse({
                    "success": False,
                    "error": "This  decoration position is not allowed in inner"
                }, status=400)
            if position == 'outer':
                if not decoration.is_outside:
                     return JsonResponse({
                    "success": False,
                    "error": "This  decoration position is not allowed in outside"
                }, status=400)
                    
                
            
            cart_item,created = CartDecoration.objects.get_or_create(cart=cart,decoration=decoration,position=position,defaults={"quantity":0})
            if cart_item.quantity > decoration.stock:
                return JsonResponse({
                    "success": False,
                    "error": "Stock is out of range. Please update your cart."
                }, status=400)
            if action == "increment":
                if position == 'inner':
                    if cart.get_used_volume() + voulme_calculater(decoration.height,decoration.width,decoration.depth) > voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth):
                        if created:
                            cart_item.delete()
                        return JsonResponse({
                            "success": False,
                            "error": "Box is Out Of Range Box Maximum Excided."
                        }, status=400)
                    print(decoration.stock,cart_item.quantity)
                    if decoration.stock > cart_item.quantity:
                        print(decoration.stock,cart_item.quantity)
                        if cart_item.position == 'outer' and cart_item.quantity >= 2:
                            return JsonResponse({
                                    "success": False,
                                    "error": "Outer only two quantity select."
                                }, status=400)
                        cart_item.quantity += 1
                    else:
                        print(decoration.stock,cart_item.quantity)
                        return JsonResponse({
                            "success": False,
                            "error": "Not enough stock available"
                        }, status=400)
                if position == 'outer':
                    
                    if not cart.cart_decoartion.filter(position='outer').count() < 3:
                        if created:
                            cart_item.delete()
                        return JsonResponse({
                            "success": False,
                            "error": "Only Two Outer Decoration You can add "
                        }, status=400)
                    if decoration.stock > cart_item.quantity:
                        if cart_item.position == 'outer' and cart_item.quantity >= 2:
                            return JsonResponse({
                                    "success": False,
                                    "error": "Outer only two quantity select. also  one outer is at a time"
                                }, status=400)
                        cart_item.quantity += 1
                    else:
                        print(decoration.stock,cart_item.quantity)
                        return JsonResponse({
                            "success": False,
                            "error": "Not enough stock available"
                        }, status=400)
                    
                
            elif action == 'decrement':
                
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    outer_count = CartDecoration.objects.filter(
                        cart=cart,
                        position="outer"
                    ).count()
                    return JsonResponse({
                            "success": True,
                            "quantity": 0,
                            "cart": {
                        "products": cart.get_products_json(),
                        "products_total": float(cart.get_products_total()),
                        "grand_total": float(cart.get_grand_total()),
                        'used_volume':float(cart.get_used_volume()),
                        'volume':float(voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth)),
                        "outer_count": outer_count  
                    }
                        })
                        
        if cart_item is not None:
            cart_item.save()

            outer_count = CartDecoration.objects.filter(
                cart=cart,
                position="outer"
            ).count()
                
            return JsonResponse({
                "success": True,
                "quantity": cart_item.quantity,
                "cart": {
                        "products": cart.get_products_json(),
                        "products_total": float(cart.get_products_total()),
                        "grand_total": float(cart.get_grand_total()),
                        'used_volume':float(cart.get_used_volume()),
                        'volume':float(voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth)),
                        "outer_count": outer_count  
                    }
            })
            
            
class CartView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        user_id = request.user.id
        if CustomUser.objects.filter(id=user_id).exists():
            user = CustomUser.objects.get(id=user_id)
            cart = {}
            cart_products = {}
            cart_decoration = {}
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                cart.volume = round( cart.box_size.height * cart.box_size.width * cart.box_size.depth / 1000,2 )
                cart.decorations_total = cart.get_decoration_total()
                cart.products_total = cart.get_products_total()
                cart.grand_total = cart.get_grand_total()
                box_image = cart.box.box_images.filter(is_thumbnail=True).first()
                if not box_image:
                    box_image = cart.box_size.box_images.all().first()
                    
                print(box_image.image)
                cart.box_image = box_image
                cart_products = cart.cart_products.all()
                
                cart_decoration = cart.cart_decoartion.all()
                # print(cart)
                # cart.grand_total = cart.box_size.price + cart.products_total + cart.decorations_total
        return render(request,'cart/cart.html',{'cart':cart,'cart_products':cart_products,'cart_decoration':cart_decoration})
    
class CartProductDelete(LoginRequiredMixin,DeleteView):
    model = CartProduct
    success_url = reverse_lazy("cart:cart_list")
    
class CartDecorationDelete(LoginRequiredMixin,DeleteView):
    model = CartDecoration
    success_url = reverse_lazy("cart:cart_list")
    
class DeleteFullCart(LoginRequiredMixin,DeleteView):
    model = CustomHamper
    success_url = reverse_lazy("cart:cart_list")
            
                
                    
                
            
        
            
        
            
        
        
        
        
        
        
        
