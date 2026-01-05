from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField
from django.views.generic import DetailView


from .models import BoxMaterial,BoxCategory,HamperBox,BoxImage,BoxSize,Product,ProductImage,ProductCategory,Decoration
from .utilts import voulme_calculater
from accounts.models import CustomUser
from core.mixins import NeverCacheMixin


class BoxListView(View):
    def get(self,request,*args, **kwargs):
        data = []
        box_types = BoxMaterial.objects.all()
        boxes_all = HamperBox.objects.all().order_by('-created_at')
        selected_boxes = request.GET.getlist('box')
        selected_categories = request.GET.getlist("category")
        selected_sizes = request.GET.getlist('sizes')
        max_price = request.GET.get('max_price','')
        sort = request.GET.get('sort','')
        selected_sizes_lower = [size.lower() for size in selected_sizes]
        print(selected_boxes)
        q = request.GET.get('search')
        if selected_categories:
            boxes_all = HamperBox.objects.filter(category__name__in=selected_categories).order_by('-created_at')
        if selected_boxes:
            boxes_all = boxes_all.filter(category__box_type__name__in=selected_boxes)
        if selected_sizes_lower:
            # print(selected_sizes_lower)
            # print(boxes_all)
            boxes_all = boxes_all.filter(sizes__size_label__in=selected_sizes_lower).distinct()
            # print(boxes_all)
        if max_price:
            boxes_all = boxes_all.filter(sizes__price__lte=max_price).distinct()
        if sort:
            if sort == 'priceLow':
                boxes_all = boxes_all.order_by('sizes__price')
                print(boxes_all)
            if sort == 'priceHigh':
                boxes_all = boxes_all.order_by('-sizes__price')
            if sort == 'name':
                boxes_all = boxes_all.order_by('name')
        if q:
            boxes_all = boxes_all.filter(name__icontains=q)
        
        box_categories = BoxCategory.objects.all()
        paginator = Paginator(boxes_all,4)
        page_number = self.request.GET.get('page')
        boxes_all =paginator.get_page(page_number)
        total_pages = paginator.num_pages
            
        total_page_num = range(1,total_pages+1)

        data = []
        size_list = BoxSize._meta.get_field('size_label').choices
        count = 0
        for i in range(len(boxes_all)):
            count += 1
            data.append({
                'box':boxes_all[i],
                'image':BoxImage.objects.filter(box_id=boxes_all[i],is_thumbnail=True).first(),
                'box_vareint':BoxSize.objects.filter(hamper_box=boxes_all[i]),
                'size':BoxSize.objects.filter(hamper_box=boxes_all[i]).first(),
                
                
            })
        return render(request,'catalog/shop-boxes.html',{'box_types':box_types,'box_categories':box_categories,'boxes':data,'size_list':size_list,'selected_boxes': selected_boxes,'selected_categories':selected_categories,'selected_sizes':selected_sizes,'total_page_num':total_page_num,'count':count})
    
    
def box_search_suggestions(request):
    q = request.GET.get('suggest','').strip()
    
    if len(q) > 1:
        
        boxes = HamperBox.objects.filter(name__icontains=q).order_by('-created_at').values('id','name')[:6]
            
        return JsonResponse({"results":list(boxes)})
    
    return JsonResponse({"results": []})


class BoxDetailView(DetailView):
    model = HamperBox
    template_name = 'catalog/box-detail.html'
    context_object_name = 'product'
    
    slug_field = "slug"
    slug_url_kwarg = 'slug'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            
            product = context.get('product')
            
        except HamperBox.DoesNotExist as e:
            print(e)
            
        context['product_images'] = BoxImage.objects.filter(box_id=product).order_by('display_order')
        sizes = BoxSize.objects.filter(hamper_box=product).order_by(
        Case(
            When(size_label='small', then=1),
            When(size_label='medium', then=2),
            When(size_label='large', then=3),
            When(size_label='extra_large', then=4),
            output_field=IntegerField(),
        
    ))
        
        for i in sizes:
            volume = round((i.width * i.height * i.depth) / 1000,2)
            i.volume = volume
        
        context['sizes'] = sizes
        
        return context


class ProductListView(NeverCacheMixin,View):
     def get(self,request,*args, **kwargs):
         products = Product.objects.all().order_by('-is_featured')
         categories = ProductCategory.objects.all()
         sort = request.GET.get('sort')
         if request.GET.get('category',''):
             filter_category = request.GET.get('category','')
             filter_category_obj = ProductCategory.objects.filter(slug=filter_category).first()
             products = products.filter(category=filter_category_obj)
             print(products,filter_category)
         if sort == 'price_asc':
            products = products.order_by('variants__price').distinct()
         if sort == 'price_desc':
             products = products.order_by('-variants__price').distinct()
         if sort == 'name_asc':
            products = products.order_by('name')
        #  print(products[0].slug) 
         q = request.GET.get('search')
         if q:
            products = products.filter(name__icontains=q)
         paginator = Paginator(products,4)
         page_number = self.request.GET.get('page')
         products =paginator.get_page(page_number)
         total_pages = paginator.num_pages
            
         total_page_num = range(1,total_pages+1)
         data = []
         user_id = request.user.id
         cart_products = []
         
         cart = []
         
         if CustomUser.objects.filter(id=user_id).exists():
            user = CustomUser.objects.get(id=user_id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                cart.volume = round( cart.box_size.height * cart.box_size.width * cart.box_size.depth / 1000,2 )
                print(cart.volume  )
                cart_products = cart.cart_products.all()
                cart.products_total = sum(
                    item.quantity * item.product_varient.price
                    for item in cart_products
                )
                cart.decorations_total = cart.get_decoration_total()

                cart.grand_total = cart.box_size.price + cart.products_total + cart.decorations_total
                
                cart_products_json = [
                    {
                        "id": item.product_varient.id,
                        "name": item.product_varient.product.name,
                        "quantity": item.quantity,
                        "price": float(item.product_varient.price),
                        "total": float(item.quantity * item.product_varient.price),
                         "variant_label": (
                                        item.product_varient.size.name
                                        if item.product_varient.size
                                        else item.product_varient.color.name
                                        if item.product_varient.color
                                        else ""
                                    ),
                        
                    }
                    for item in cart_products
                ]
                cart_decorations_json = [
                        {
                            "name": d.decoration.name,
                            "quantity": d.quantity,
                            "price": float(d.decoration.price),
                            "total": float(d.quantity * d.decoration.price),
                            'position':d.position
                        }
                        for d in cart.cart_decoartion.all()
                    ]
                
                cart.used_volume =cart.get_used_volume()
                
            
         
         for product in products:
            if product.variants.first():
                image = product.variants.first().variants_images.filter(is_thumbnail=True).first()
                if not image:
                    image = product.variants.first().variants_images.first()
                variant = product.variants.first()
                  
                volume = round(variant.width * variant.height * variant.depth / 1000,2)
                qty = 0
                if cart_products:
                    cart_item = cart_products.filter(product_varient=variant).first()
                    if cart_item:
                        qty = cart_item.quantity
                        
                
                data.append({'product':product,'varient':variant,'image':image,'volume':volume,'selected_qty':qty})
                # print(image)
                # print(data[0]['image'].image)
        
            
         
         return render(request,'catalog/product_list.html',{'data':data,'categories':categories,'total_page_num':total_page_num,'cart':cart,'cart_products_json':cart_products_json,'cart_decorations_json':cart_decorations_json,})


def product_search_suggestions(request):
    q = request.GET.get('suggest','').strip()
    
    if len(q) > 1:
        
        products = Product.objects.filter(name__icontains=q).order_by('-created_at').values('id','name')[:6]
            
        return JsonResponse({"results":list(products)})
    
    return JsonResponse({"results": []})


class ProductDetailView(DetailView):
    
    model = Product
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    
    slug_field = "slug"
    slug_url_kwarg = 'slug'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            
            product = context.get('product')
            
        except Product.DoesNotExist as e:
            print(e)
        
        varients = product.variants.all()
        
        user_id = self.request.user.id
        cart_products = []
        cart_decoations = []
        cart = []
         
        if CustomUser.objects.filter(id=user_id).exists():
            user = CustomUser.objects.get(id=user_id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                cart.volume = round( cart.box_size.height * cart.box_size.width * cart.box_size.depth / 1000,2 )
                print(cart.volume  )
                cart_products = cart.cart_products.all()
                cart.products_total = sum(
                    item.quantity * item.product_varient.price
                    for item in cart_products
                )

                cart.grand_total = cart.box_size.price + cart.products_total
                
                cart_products_json = [
                    {
                        "id": item.product_varient.id,
                        "name": item.product_varient.product.name,
                        "quantity": item.quantity,
                        "price": float(item.product_varient.price),
                        "total": float(item.quantity * item.product_varient.price),
                        "variant_label": (
                                        item.product_varient.size.name
                                        if item.product_varient.size
                                        else item.product_varient.color.name
                                        if item.product_varient.color
                                        else ""
                                    ),
                        
                    }
                    for item in cart_products
                ]
                cart_decoations = cart.cart_decoartion.all()
                cart.used_volume =cart.get_used_volume()
                
        
        varient_data = []
        for i in varients:
            varient_data.append({
                'varient':i,
                'images':i.variants_images.order_by('display_order'),
                'volume':voulme_calculater(i.height,i.width,i.depth)
            })
        if  varient_data[0]['varient'].size:
            size_color = 'size'
        elif  varient_data[0]['varient'].color:
            size_color = 'color'
        else:
            size_color = False
        context['size_color'] =  size_color
        context['varients'] = varient_data
        context['cart_products_json'] =cart_products_json if cart_products_json else None
        context['cart'] = cart if cart else None
        context['cart_decoations'] = cart_decoations if cart_decoations else None
        return context


class DecorationListView(View):
    def get(self,request,*args, **kwargs):
        list_decor= Decoration.objects.all()
        location = request.GET.get('location')
        max_price = request.GET.get('max_price')

        if max_price:
            list_decor = list_decor.filter(price__lte=max_price)
        if location == 'outer':
            list_decor = list_decor.filter(is_outside=True,is_inside=False)

        if location == 'inner':
            list_decor = list_decor.filter(is_inside=True,is_outside=False)
            
        if location == 'both':
            list_decor = list_decor.filter(is_inside=True,is_outside=True)
        
        q = request.GET.get('search')
        if q:
            list_decor = list_decor.filter(name__icontains=q)
            
        sort = request.GET.get("sort")
        print(sort)
        if sort == "price_low":
            list_decor = list_decor.order_by("price")

        elif sort == "price_high":
            list_decor = list_decor.order_by("-price")

        #  elif sort == "popular":
        #     pass  

        # elif sort == "rating":
            # pass

        else:  # newest
            list_decor = list_decor.order_by("-created_at")
            
        paginator = Paginator(list_decor,4)
        page_number = self.request.GET.get('page')
        list_decor =paginator.get_page(page_number)
        total_pages = paginator.num_pages
            
        total_page_num = range(1,total_pages+1)
        user_id = request.user.id
        cart_products = []
        cart_decoations = []
        cart = []
         
        
        if CustomUser.objects.filter(id=user_id).exists():
            user = CustomUser.objects.get(id=user_id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                cart.volume = round( cart.box_size.height * cart.box_size.width * cart.box_size.depth / 1000,2 )
                print(cart.volume  )
                cart_products = cart.cart_products.all()
                cart.products_total = sum(
                    item.quantity * item.product_varient.price
                    for item in cart_products
                )
                cart.decorations_total = cart.get_decoration_total()

                cart.grand_total = cart.box_size.price + cart.products_total + cart.decorations_total
                
                cart_products_json = [
                    {
                        "id": item.product_varient.id,
                        "name": item.product_varient.product.name,
                        "quantity": item.quantity,
                        "price": float(item.product_varient.price),
                        "total": float(item.quantity * item.product_varient.price),
                         "variant_label": (
                                        item.product_varient.size.name
                                        if item.product_varient.size
                                        else item.product_varient.color.name
                                        if item.product_varient.color
                                        else ""
                                    ),
                        
                    }
                    for item in cart_products
                ]
                cart_decorations_json = [
                        {
                            "name": d.decoration.name,
                            "quantity": d.quantity,
                            "price": float(d.decoration.price),
                            "total": float(d.quantity * d.decoration.price),
                            'position':d.position
                        }
                        for d in cart.cart_decoartion.all()
                    ]
                
                cart.used_volume =cart.get_used_volume()

        decorations = []
        count = 0
        for i in list_decor:
            count +=1
            image= i.decoartion_image.filter(is_thumbnail=True).first()
            if not image:
                image = i.decoartion_image.all().first()
            decorations.append({'product':i,'image':image})

        return render(request,'catalog/shop-decorations.html',{'decorations':decorations,'count':count,'total_page_num':total_page_num,'cart':cart,'cart_products_json':cart_products_json,'cart_decorations_json':cart_decorations_json,})
        
        
        
def decoartion_search_suggestions(request):
    q = request.GET.get('suggest','').strip()
    
    if len(q) > 1:
        
        products = Decoration.objects.filter(name__icontains=q).order_by('-created_at').values('id','name')[:6]
            
        return JsonResponse({"results":list(products)})
    
    return JsonResponse({"results": []})
            
            
            
            

class DecorationDetailView(DetailView):
    
    model = Decoration
    template_name = 'catalog/decoration-detail.html'
    context_object_name = 'product'
    
    slug_field = "slug"
    slug_url_kwarg = 'slug'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            
            decoartor = context.get('product')
            
        except Decoration.DoesNotExist as e:
            print(e)
        volume = round(decoartor.width * decoartor.height * decoartor.depth / 1000 , 2)
        user_id = self.request.user.id
        if CustomUser.objects.filter(id=user_id).exists():
            user = CustomUser.objects.get(id=user_id)
            if hasattr(user,'current_cart'):
                cart = user.current_cart
                cart_volume = cart.get_used_volume()
                cart_max_volume = voulme_calculater(cart.box_size.height,cart.box_size.width,cart.box_size.depth)
                outer_count = cart.cart_decoartion.filter(position='outer').count()
                inner_qty = 0
                outer_selected = False
                this_inner = cart.cart_decoartion.filter(decoration=decoartor,position='inner').first()
                this_outer = cart.cart_decoartion.filter(decoration=decoartor,position='outer').first()
                if this_inner:
                    inner_qty = this_inner.quantity
                if this_outer:
                    outer_selected = True if this_outer.quantity >= 1 else False
                
        
        context['volume'] = volume
        context['images'] = decoartor.decoartion_image.all()
        context['cart_volume'] = cart_volume
        context['cart_max_volume'] = cart_max_volume
        context['outer_count'] = outer_count
        context.update({
            "inner_qty": inner_qty,
            "outer_selected": outer_selected,
        })
        return context