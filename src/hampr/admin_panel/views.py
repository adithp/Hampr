from django.shortcuts import render
from django.views.generic import TemplateView,DeleteView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from accounts.models import CustomUser
from django.db.models import Q
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from itertools import chain


from .mixins import StaffRequiredMixin,LoginInRedirectMixin
from core.mixins import NeverCacheMixin
from .forms import HamperBoxForm,BoxTypeForm,BoxCategoryAdd,BoxSizeForm,ProductCategoryForm,ProductForm,ProductSimpleVairentForm,ColorForm,SizeForm,DecorationForm
from catalog.models import BoxCategory,BoxMaterial,HamperBox,BoxCategoryImage,BoxSize,BoxImage,ProductCategory,Product,Color,Size,ProductVariant,ProductImage,DecorationImages,Decoration



class AdminLoginView(NeverCacheMixin,LoginInRedirectMixin,View):
     def get(self, request, *args, **kwargs):
        return render(request,'c_admin/admin_login.html')
    
     def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(Q(username=identifier)| Q(email=identifier))
        except CustomUser.DoesNotExist:
            messages.error(request,"Invalid Username")
            return redirect(reverse_lazy('cadmin:admin_login'))
        if not user.check_password(password):
            messages.error(request,"password invalid")
            return redirect(reverse_lazy('cadmin:admin_login'))
        if not user.is_active:
            messages.error(request,"Contact superadmin admin blocked by superadmin")
            return redirect(reverse_lazy('cadmin:admin_login'))
        
        if not user.is_staff:
            messages.error(request,"only admin can access")
            return redirect(reverse_lazy('cadmin:admin_login'))
        user.backend = 'django.contrib.auth.backends.ModelBackend'  
        login(request,user)
        return redirect('cadmin:admin_dashboard')


class AdminDashboardView(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_count = CustomUser.objects.filter(is_superuser=False,is_staff=False).count()
        active_users = CustomUser.objects.filter(is_superuser=False,is_staff=False,is_active=True).count()
        blocked_users =  CustomUser.objects.filter(is_superuser=False,is_staff=False,is_active=False).count()
        context['users_count'] = users_count
        context['active_users'] = active_users
        context['blocked_users'] = blocked_users
        
        return context
    

class AdminUserManagement(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/user_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.objects.filter(is_superuser=False,is_staff=False)
        query = self.request.GET.get('q',{})
        if query:
            users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))
        
        paginator = Paginator(users,8)
        page_number = self.request.GET.get('page')
        users =paginator.get_page(page_number)
        total_pages = paginator.num_pages
            
        context['total_page_num'] = range(1,total_pages+1)

        context['users_list'] = users
        
        return context
    
    
class AdminBlockUser(StaffRequiredMixin,View):
    
    def get(self,request,id,*args, **kwargs):
        try:
            user = CustomUser.objects.get(id=id)
        except:
            pass
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        q = request.GET.get('search','')
        page = request.GET.get('page','')
        print(request.GET.urlencode)
        print(q)
        return redirect(reverse('cadmin:user_management')+ f"?search={q}&page={page}")
    
    
class AdminProductsMainPage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        for i in  BoxSize.objects.filter(stock__lt = 6):
            i.item_type = 'Box'
            data.append(i)
        for i in  ProductVariant.objects.filter(stock__lt = 6):
            i.item_type = 'Interior'
            data.append(i)
        for i in Decoration.objects.filter(stock__lt = 6):
            i.item_type = 'Decor'
            data.append(i)   
        print(data)
        
        paginator = Paginator(data,2)
        page_number = self.request.GET.get('pagelow')
        low_products =paginator.get_page(1000)
        total_pages = paginator.num_pages
            
        context['total_page_num'] = range(1,total_pages+1)

        context['low_products'] = low_products
        print(low_products)
        
        return context
    
    
    
class AdminBoxProductsMainPage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-boxes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        q =  self.request.GET.get('search','')
        if q:
            boxess = HamperBox.objects.filter(name__icontains=q)
        else:
            boxess = HamperBox.objects.all()
        paginator = Paginator(boxess,4)
        page_number = self.request.GET.get('page')
        boxes = paginator.get_page(page_number)
        total_pages = paginator.num_pages
       
        data = []
        for i in range(len(boxes)):
            image = BoxImage.objects.filter(is_thumbnail=True,box_id=boxes[i]).first()
            box_sizes = BoxSize.objects.filter(hamper_box=boxes[i])
            data.append({'box':boxes[i],'image':image,'sizes':box_sizes})
        context['datas'] = data
        context['total_page_num'] = range(1,total_pages+1)

        return context
    
    
class AdminBoxTypeManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-box-types.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q =  self.request.GET.get('search','')
        if q:
            box_types = BoxMaterial.objects.filter(name__icontains=q)
        else:
            box_types = BoxMaterial.objects.all()
        paginator = Paginator(box_types,4)
        page_number = self.request.GET.get('page')
        box_types = paginator.get_page(page_number)
        total_pages = paginator.num_pages
    
        context['box_types'] = box_types
        context['total_page_num'] = range(1,total_pages+1)
        return context
    
    
class AdminBoxCategoryManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-box-categories.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q =  self.request.GET.get('search','')
        if q:
            box_categories = BoxCategory.objects.filter(name__icontains=q)
        else:
            box_categories = BoxCategory.objects.all()
        paginator = Paginator(box_categories,4)
        page_number = self.request.GET.get('page')
        box_categories = paginator.get_page(page_number)
        total_pages = paginator.num_pages
        context['total_page_num'] = range(1,total_pages+1)
        context['box_categories'] = box_categories
        return context
    
    
class AdminBoxTypeItemAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        form = BoxTypeForm()
        return render(request,'c_admin/admin-products-box-types-add.html',{'form':form,})
    
    def post(self,request,*args, **kwargs):
        data = request.POST
        form = BoxTypeForm(data)
        if form.is_valid():
            form.save()
            return redirect('cadmin:box_type_manage')
        else:
            return render(request,'c_admin/admin-products-box-types-add.html',{'form':form})


class AdminBoxCategoryItemAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        form = BoxCategoryAdd()
        return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':False})
    
    def post(self,request,*args, **kwargs):
        data = request.POST
        files = request.FILES.getlist('images')
        print(files)
        orders = data.getlist('orders')
        primary = data.getlist('primary')
        form = BoxCategoryAdd(data)
        if len(files) != len(orders) or len(files) != len(primary):
            form.add_error(None, "Invalid image order or primary values.")
            return render(request, 'c_admin/admin-products-box-categories-add.html', {'form': form})
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj =  form.save()
                    for i in range(len(orders)):
                        if files[i].size >  (5*1024*1024):
                            form.add_error('Image size is under 5mb')
                            return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form})
                        
                        image_obj = BoxCategoryImage(box_category=obj,display_order=orders[i],image=files[i],is_primary=True if int(primary[i]) else False)
                        image_obj.save()
                        
                        
                    
                return redirect('cadmin:box_type_manage')
            except ValidationError as e:
                form.add_error(None, str(e))
                return render(request, 'c_admin/admin-products-box-categories-add.html', {'form': form})

            except Exception:
                form.add_error(None, "Something went wrong while saving images.")
                return render(request, 'c_admin/admin-products-box-categories-add.html', {'form': form})
                    
        else:
            return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form})
    
    
class AdminBoxProductsAddItem(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        pen = request.session.get('product_add_first_stage_id',{})
        print(pen)
        if pen:
            return redirect('cadmin:add_box_second')
        
        form = HamperBoxForm()
        return render(request,'c_admin/admin-products-boxes-add-step1.html',{'form':form,})
    
    def post(self,request,*args, **kwargs):
        form = HamperBoxForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            obj = form.save()
            request.session['product_add_first_stage_id'] = str(obj.id)
            return redirect('cadmin:add_box_second')
        
        
        else:
            return render(request,'c_admin/admin-products-boxes-add-step1.html',{'form':form,})
        
    
class AdminBoxProductsAddItemSecond(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if not request.session.get('product_add_first_stage_id',{}):
            messages.error(request,'First You nedd to complete first phase')
            return redirect('cadmin:add_box_first_phase')
        
        form = BoxSizeForm()
        return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,})
    
    def post(self,request,*args, **kwargs):
        if not request.session.get('product_add_first_stage_id',{}):
            messages.error(request,'First You nedd to complete first phase')
            return redirect('cadmin:add_box_first_phase')
              
        form = BoxSizeForm(request.POST)
        
        if form.is_valid():
            hamper_box_id=request.session.get('product_add_first_stage_id')
            
            hamper_box = HamperBox.objects.get(id=hamper_box_id)
            size_label = form.cleaned_data.get('size_label')
            if BoxSize.objects.filter(hamper_box=hamper_box,size_label=size_label).exists():
                form.add_error('size_label','this size already added')
                return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,})
            wait = form.save(commit=False)
            wait.hamper_box = hamper_box
            wait.save()
            messages.success(request,'Product Added Succsesfully')
            return redirect('cadmin:add_box_second')
        return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,})
    
    
def redirect_to_image_upload_box(request):
    if not request.session.get('product_add_first_stage_id',{}):
        messages.error(request,'First You nedd to complete first phase')
        return redirect('cadmin:add_box_first_phase')
    
    
    request.session['product_add_second_stage_id'] = request.session.get('product_add_first_stage_id')
    
    return redirect('cadmin:add_box_third')


def productBox_adding_cancel(request):
    id = request.session.get('product_add_first_stage_id',{})
    box = HamperBox.objects.get(id=id)
    box.delete()
    return redirect('cadmin:box_manage')

   
class AdminBoxProductsAddItemThird(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if not request.session.get('product_add_second_stage_id',{}):
            messages.error(request,'First You nedd to complete first phase')
            messages.error(request,'\nComplete Second Phase')
            return redirect('cadmin:add_box_second')
        return render(request,'c_admin/admin-products-boxes-add-step3.html')
    
    def post(self,request,*args, **kwargs):
        if not request.session.get('product_add_second_stage_id',{}):
            messages.error(request,'First You nedd to complete first phase')
            messages.error(request,'\nComplete Second Phase')
            return redirect('cadmin:add_box_second')
        print(request.POST,request.FILES)
        hamper_id  = request.session.get('product_add_second_stage_id')
        hamper_box = HamperBox.objects.get(id=hamper_id)
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        images = request.FILES.getlist('images')
        
        if len(orders) != len(primary) or len(primary) != len(images):
            messages.error(request,'image upload error')
            return render(request,'c_admin/admin-products-boxes-add-step3.html')
        
        try:
            with transaction.atomic():
                for i in range(len(orders)):
                    if images[i].size >  (5*1024*1024):
                            messages.error(request,'Image size must Under 5mb')
                            return render(request,'c_admin/admin-products-boxes-add-step3.html')
                    obj = BoxImage(display_order=orders[i],image=images[i],is_thumbnail= True if primary[i] == '1' else False,box_id=hamper_box)
                    obj.save()
        except ValidationError as e:
            messages.error(request,'smothing happen when image upload')
            return render(request,'c_admin/admin-products-boxes-add-step3.html')

        except Exception:
            messages.error(request,'smothing happen when image upload')
            return render(request,'c_admin/admin-products-boxes-add-step3.html')
            
        del request.session['product_add_first_stage_id'] 
        del request.session['product_add_second_stage_id'] 
        return redirect('cadmin:box_manage')
    
      
class AdminProductAddCategory(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        form = ProductCategoryForm()
        return render(request,'c_admin/admin_products_interior_category_add.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'product category added')
            return redirect('cadmin:add_product_category')
        else:
            return render(request,'c_admin/admin_products_interior_category_add.html',{'form':form})    
        
        
class AdminProductCategoryManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin_products_interior_category_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q =  self.request.GET.get('search','')
        if q:
            product_categories = ProductCategory.objects.filter(name__icontains=q)
        else:
            product_categories = ProductCategory.objects.all()          
        paginator = Paginator(product_categories,4)
        page_number = self.request.GET.get('page')
        product_categories =paginator.get_page(page_number)
        total_pages = paginator.num_pages
        context['total_page_num'] = range(1,total_pages+1)
        context['product_categories'] = product_categories
        return context
    
    
     
        

class AdminProductManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-interior.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q =  self.request.GET.get('search','')
        if q:
            products = Product.objects.filter(name__icontains=q)
        else:
             products = Product.objects.all()
        paginator = Paginator(products,4)
        page_number = self.request.GET.get('page')
        products =paginator.get_page(page_number)
        total_pages = paginator.num_pages
        context['total_page_num'] = range(1,total_pages+1)
        data = [
            
        ]
        for i in products:
            data.append({   
                'product':i,
                'varients':[{'varient':j,'image':ProductImage.objects.filter(product=j,is_thumbnail=True).first()} for j in ProductVariant.objects.filter(product=i)] 
            })
        context['data'] = data
        return context
    
            

        
class AdminProductAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        categories = ProductCategory.objects.all()
        form = ProductForm()
        return render(request,'c_admin/admin-products-interior-add.html',{'categories':categories,'form':form})
    
    def post(self,request,*args, **kwargs):
        data = request.POST
        
        form = ProductForm(data)
        print(data)
        if form.is_valid():
            
            obj = form.save()
            request.session['pending_product_add_id'] = obj.id
            return redirect('cadmin:varient_or_not')
            
        else:
            categories = ProductCategory.objects.all()
            print(form.errors)
            return render(request,'c_admin/admin-products-interior-add.html',{'categories':categories,'form':form})
        
        
class AdminProductSimpleVarientAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if not request.session.get('pending_product_add_id'):
            return redirect('cadmin:product_add')
        form = ProductSimpleVairentForm()
        return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form})
    def post(self,request,*args, **kwargs):
        pending_id =  request.session.get('pending_product_add_id')
        if not pending_id:
            return redirect('cadmin:product_add')
        
        try:
            product = Product.objects.get(id=pending_id)
        except:
            pass  ## add 404 error 
        form = ProductSimpleVairentForm(request.POST)
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        if len(orders) != len(primary) or len(orders) != len(files):
            form.add_error(None, 'Image Upload has some issue')
            return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form})
        print(request.POST)
        if form.is_valid():
            commit_form = form.save(commit=False)
            commit_form.product = product
            commit_form.is_default = True
            
            commit_form.save()
            variant_id = commit_form.id
            variant_obj = ProductVariant.objects.get(id=variant_id)
            
            try:
                for i in range(len(files)):
                    img_obj = ProductImage(product=variant_obj,display_order=int(orders[i]),is_thumbnail=True if primary[i] == '1' else False,image=files[i] )
                    img_obj.save()
                
            except Exception as e:
                print(e)
            del request.session['pending_product_add_id']
            return redirect('cadmin:interior_product_manage')
        else:
            print(form.errors)                
            return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form})
 

class AdminProductVarientAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if not request.session.get('pending_product_add_id'):
            return redirect('cadmin:product_add')
        form = ProductSimpleVairentForm()
        color = ColorForm()
        size_form = SizeForm()
        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color,'size_form':size_form})
    def post(self,request,*args, **kwargs):
        pending_id =  request.session.get('pending_product_add_id')
        if not pending_id:
            return redirect('cadmin:product_add')
        print(request.POST)
        print(request.FILES)
        
        data = request.POST
        form = ProductSimpleVairentForm(request.POST)
        if request.POST.get('variant_type_variant-1') == 'Color':
            colorhex = request.POST.get('variant_color_code_variant-1') 
            color_name = request.POST.get('variant_color_variant-1')
            color_form = ColorForm(data={'hex':colorhex,'name':color_name})
            product = Product.objects.filter(id=pending_id).first()
            if ProductVariant.objects.filter(product=product,color__name__iexact=color_name).exists():
                        messages.error(request,'The Color Already added')
                        return redirect('cadmin:products_varients_add_extra')
            try:
                with transaction.atomic():
                    if color_form.is_valid():
                        color = color_form.save()
                        response =  self.updating_data(request=request,pending_id=pending_id,color=color,color_form=color_form)
                        return response
                    else:
                                    
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form})
            except Exception as e:
                 print("Error:", e)
                 messages.error(request, "Something went wrong. Please try again.")
                 return redirect('cadmin:products_varients_add_extra')
        else:
            try:
                with transaction.atomic():
                    size_form = SizeForm(data={
                        'name':request.POST.get('variant_size_variant-1'),
                        'sort_order':int(request.POST.get('variant_size_order_variant-1'))
                        
                    })
                    product = Product.objects.filter(id=pending_id).first()
                    if ProductVariant.objects.filter(product=product,size__name__iexact=request.POST.get('size')).exists():
                        messages.error(request,'The Size Already added')
                        return redirect('cadmin:products_varients_add_extra')
                    if size_form.is_valid():
                        size_obj = size_form.save()
                        response = self.updating_data(request=request,pending_id=pending_id,size=size_obj,size_form=size_form)
                        return response 
                    else:
                        print(size_form.errors)
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'size_form':size_form})
            except Exception as e:
                 print("Error:", e)
                 messages.error(request, "Something went wrong. Please try again.")
                 return redirect('cadmin:products_varients_add_extra')
            
            
    def updating_data(self,request,pending_id,color=None,size=None,color_form=None,size_form=None):
        
        try:
            product = Product.objects.get(id=pending_id)
        except:
            print('inside going ')
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('cadmin:products_varients_add_extra')
        form = ProductSimpleVairentForm(request.POST)
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        if len(orders) != len(primary) or len(orders) != len(files):
            form.add_error(None, 'Image Upload has some issue')
            return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form})
        print(request.POST)
        form.instance.product = product
        if color:
            form.instance.color = color
        elif size:
            form.instance.size = size
        if form.is_valid():
            commit_form = form.save(commit=False)
            
            commit_form.is_default = True
            
            commit_form.save()
            variant_id = commit_form.id
            variant_obj = ProductVariant.objects.get(id=variant_id)
                
            try:
                for i in range(len(files)):
                    img_obj = ProductImage(product=variant_obj,display_order=int(orders[i]),is_thumbnail=True if primary[i] == '1' else False,image=files[i] )
                    img_obj.save()
                
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong. Please try again.")
            return redirect('cadmin:products_varients_add_extra') 
        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form}) 
           
        
    
    
def varient_or_not(request):
    if not request.session.get('pending_product_add_id'):
            return redirect('cadmin:product_add')
    return render(request,'c_admin/admin-products-interior-variant-selection.html')


def varients_finshed(request):
    penidng_id = request.session['pending_product_add_id']
    product = Product.objects.filter(id=penidng_id).first()
    if not ProductVariant.objects.filter(product=product).exists():
        messages.error(request,"Minimum One Varient is mandatory")
        return redirect('cadmin:products_varients_add_extra')
    del request.session['pending_product_add_id']
    return redirect('cadmin:interior_product_manage')
    
           
def cancel_add_product(req):
    if req.method == 'POST':
        pending_id = req.session.get('pending_product_add_id')
        product = Product.objects.filter(id=pending_id).first()
        del product
        return redirect('cadmin:interior_product_manage')
    
    
class AdminDecorationAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        form = DecorationForm()
        return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'edit':False})
    
    def post(self,request,*args, **kwargs):
        print(request.POST)
        print(request.FILES)
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        
        form = DecorationForm(request.POST)
        if len(orders) != len(primary) or len(orders) != len(files):
            form.add_error(None, 'Image Upload has some issue')
            return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'edit':False,})
        if form.is_valid():
            obj = form.save()
            try:
                for i in range(len(files)):
                    img_obj = DecorationImages(product=obj,display_order=int(orders[i]),is_thumbnail=True if primary[i] == '1' else False,image=files[i] )
                    img_obj.save()
                
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong. Please try again.")
            
            return redirect('cadmin:decoration_manage')
        return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'edit':False})
    
    
class AdminDecortionManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-decorations.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q =  self.request.GET.get('search','')
        if q:
            decoration = Decoration.objects.filter(name__icontains=q)
        else:
             decoration = Decoration.objects.all()
        paginator = Paginator(decoration,4)
        page_number = self.request.GET.get('page')
        decoration =paginator.get_page(page_number)
        total_pages = paginator.num_pages
        
    
        data = [
            
        ]
        for i in range(len(decoration)):
            data.append({
                'product':decoration[i],
                'image':DecorationImages.objects.filter(product=decoration[i],is_thumbnail=True).first()
            })
        context['data'] = data
        context['total_page_num'] = range(1,total_pages+1)
        return context
    
    
class AdminBoxTypeDelete(DeleteView):
    model = BoxMaterial
    success_url = reverse_lazy('cadmin:box_type_manage')
    
    
class AdminBoxCategoryDelete(DeleteView):
    model = BoxCategory 
    success_url = reverse_lazy('cadmin:box_category_manage')
    
    
class AdminMainProductDelete(DeleteView):
    model = HamperBox
    success_url = reverse_lazy('cadmin:box_manage')
    
    
class AdminBoxDelete(DeleteView):
    model = BoxSize
    success_url = reverse_lazy('cadmin:box_manage')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()

        if ProductVariant.objects.filter(product=obj.product).count() == 1:
            product = obj.product
            product.delete()
            return redirect(reverse_lazy('cadmin:box_manage'))
            

        return super().delete(request, *args, **kwargs)
    
    
class AdminProductCategoryDelete(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('cadmin:products_category_list')
    
    
class AdminProductVarientDelete(DeleteView):
    model = ProductVariant
    success_url = reverse_lazy('cadmin:interior_product_manage')
   
    
class AdminProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('cadmin:interior_product_manage')
    
 
class AdminDecorationDelete(DeleteView):
    model = Decoration
    success_url = reverse_lazy('cadmin:decoration_manage')
    
    
class AdminBoxCategoryItemEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        box_category = BoxCategory.objects.get(id=id)
        form = BoxCategoryAdd(instance=box_category)
        existing_images = BoxCategoryImage.objects.filter(box_category=box_category)
        return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
    
    def post(self,request,id,*args, **kwargs):
        data = request.POST
        files = request.FILES.getlist('images')
        print(data)
        print(files)
        
        orders = data.getlist('orders')
        primary = data.getlist('primary')
        seq_types  = data.getlist('seq_types')
        existing_ids = data.getlist('existing_ids')
        deleted_ids = data.getlist('deleted_ids')
        box_category = BoxCategory.objects.get(id=id)
        form = BoxCategoryAdd(data=data,instance=box_category)
        existing_images = BoxCategoryImage.objects.filter(box_category=box_category)
        if  len(orders)!= len(primary) and len(orders) != len(seq_types):
            form.add_error(None, "Invalid image order or primary values.")
            return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
        if form.is_valid():
            count = 0
            try:
                with transaction.atomic():
                    obj =  form.save()
                    for i in range(len(orders)):
                        if seq_types[i] == 'existing':
                            image_id =existing_ids.pop(0)
                            try:
                                image_obj = BoxCategoryImage.objects.get(id=image_id)
                                
                            except BoxCategoryImage.DoesNotExist:
                                continue
                            image_obj.display_order = orders[i]
                            image_obj.is_primary = is_primary=True if int(primary[i]) else False
                            image_obj.save() 
                        else:  
                                                    
                            if files[count].size >  (5*1024*1024):
                                form.add_error('Image size is under 5mb')
                                return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
                            
                            image_obj = BoxCategoryImage(box_category=obj,display_order=orders[i],image=files[count],is_primary=True if int(primary[i]) else False)
                            image_obj.save()
                            count+=1
                    for i in deleted_ids:
                        try:
                            im_obj = BoxCategoryImage.objects.get(id=i)
                            
                        except BoxCategoryImage.DoesNotExist:
                            print('Delete Object Not Showing')
                        im_obj.delete()
                    messages.success(request, "Box Category Updated  successfully!")
                    return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
            except ValidationError as e:
                form.add_error(None, str(e))
                return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})

            except Exception:
                form.add_error(None, "Something went wrong while saving images.")
                return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
                    
        else:
            return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,'edit_mode':True,'existing_images':existing_images})
        
        
class AdminBoxTypeItemEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        try:
            box_type = BoxMaterial.objects.get(id=id)
        except BoxMaterial.DoesNotExist as e:
            print(e)
            
        form = BoxTypeForm(instance=box_type)
        return render(request,'c_admin/admin-products-box-types-add.html',{'form':form,})
    
    def post(self,request,id,*args, **kwargs):
        data = request.POST
        try:
            box_type = BoxMaterial.objects.get(id=id)
        except BoxMaterial.DoesNotExist as e:
            print(e)
            
        form = BoxTypeForm(data,instance=box_type)
        if form.is_valid():
            form.save()
            
            return redirect('cadmin:box_type_manage')
        else:
            return render(request,'c_admin/admin-products-box-types-add.html',{'form':form})
        
         
class AdminBoxProductsEditItem(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        
        try:
            hamper_box = HamperBox.objects.get(id=id)
        except HamperBox.DoesNotExist as e:
            print(e)
            
        form = HamperBoxForm(instance=hamper_box)
        return render(request,'c_admin/admin-products-boxes-add-step1.html',{'form':form,'edit':True})
    
    def post(self,request,id,*args, **kwargs):
        try:
            hamper_box = HamperBox.objects.get(id=id)
        except HamperBox.DoesNotExist as e:
            print(e)
        form = HamperBoxForm(request.POST,instance=hamper_box)
        print(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            obj = form.save()
            
            return redirect('cadmin:box_manage')
        
        
        else:
            return render(request,'c_admin/admin-products-boxes-add-step1.html',{'form':form,'edit':True})

             
class AdminBoxProductsEditItemSecond(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        box_size = BoxSize.objects.get(id=id)
        form = BoxSizeForm(instance=box_size)
        return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,'edit':True})
    
    def post(self,request,id,*args, **kwargs):
        box_size = BoxSize.objects.get(id=id)
        form = BoxSizeForm(request.POST,instance=box_size)
        
        if form.is_valid():
            size_label = form.cleaned_data.get('size_label')
            if BoxSize.objects.filter(hamper_box=box_size.hamper_box,size_label=size_label).exclude(id=box_size.id).exists():
                form.add_error('size_label','this size already added')
                return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,})
            form.save()
            
            return redirect('cadmin:box_manage')
        return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,'edit':True})
    
     
class AdminBoxProductsEditItemThird(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        images = BoxImage.objects.filter(box_id=id)
        context = {
            'edit':True,
            'existing_images':images
        }
        
        return render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
    
    def post(self,request,id,*args, **kwargs):
    
        context = {
            'edit':True,
            'existing_images':BoxImage.objects.filter(box_id=id)
        }
        print(request.POST,request.FILES)
        try:
            hamper_box = HamperBox.objects.get(id=id)
        except HamperBox.DoesNotExist as e:
            print(e)
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        images = request.FILES.getlist('images')
        seq_types = request.POST.getlist('seq_types')
        existing_ids = request.POST.getlist('existing_ids')
        deleted_ids = request.POST.getlist('deleted_ids',[])
        
        if  len(orders)!= len(primary) and len(orders) != len(seq_types):
            messages.error(request, "Invalid image order or primary values.")
            return render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
        
        try:
            with transaction.atomic():
                count = 0
                for i in range(len(seq_types)):
                    if seq_types[i] == 'existing':
                        ex_image_obj = BoxImage.objects.get(id=existing_ids[i])
                        ex_image_obj.display_order = orders[i]
                        ex_image_obj.is_thumbnail = True if primary[i] == '1' else False
                    else: 
                        if images[count].size >  (5*1024*1024):
                            messages.error(request,'Image size must Under 5mb')
                            return render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
                        obj = BoxImage(display_order=orders[i],image=images[count],is_thumbnail= True if primary[i] == '1' else False,box_id=hamper_box)
                        obj.save()
                        count += 1
                for i in deleted_ids:
                    del_img = BoxImage.objects.get(id=i)
                    del_img.delete()
                
                    
        
        except ValidationError as e:
            messages.error(request,'smothing happen when image upload')
            return render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
       
        except Exception:
            messages.error(request,'smothing happen when image upload')
            return render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
            
        messages.success(request,'Update succsessfully')
        return  render(request,'c_admin/admin-products-boxes-add-step3.html',context=context)
    
    
class AdminProductEditCategory(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,slug,*args, **kwargs):
        try:
            instance = ProductCategory.objects.get(slug=slug)
        except ProductCategory.DoesNotExist as e:
            print(e)
        form = ProductCategoryForm(instance=instance)
        return render(request,'c_admin/admin_products_interior_category_add.html',{'form':form,'edit':True})
    
    def post(self,request,slug,*args, **kwargs):
        try:
            instance = ProductCategory.objects.get(slug=slug)
        except ProductCategory.DoesNotExist as e:
            print(e)
        form = ProductCategoryForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request,'product category updated')
            
        
        return render(request,'c_admin/admin_products_interior_category_add.html',{'form':form,'edit':True})  
    
    
class AdminProductEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        categories = ProductCategory.objects.all()
        try:
            instance = Product.objects.get(id=id)
        except Product.DoesNotExist as e:
            print(e)
        form = ProductForm(instance=instance)
        return render(request,'c_admin/admin-products-interior-add.html',{'categories':categories,'form':form,'edit':True,'product':instance})
    
    def post(self,request,id,*args, **kwargs):
        categories = ProductCategory.objects.all()
        try:
            instance = Product.objects.get(id=id)
        except Product.DoesNotExist as e:
            print(e)
        data = request.POST
        
        form = ProductForm(data,instance=instance)
        
        if form.is_valid():
            
            obj = form.save()
            messages.success(request,'product Update successfull')
            return render(request,'c_admin/admin-products-interior-add.html',{'categories':categories,'form':form,'edit':True,'product':instance})
            
        else:
            categories = ProductCategory.objects.all()
            
            return render(request,'c_admin/admin-products-interior-add.html',{'categories':categories,'form':form,'edit':True,'product':instance})


class AdminProductSimpleVarientEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        try:
            instance = ProductVariant.objects.get(id=id)
        except ProductVariant.DoesNotExist as e:
            print(e)
        form = ProductSimpleVairentForm(instance=instance)
        existing_images = ProductImage.objects.filter(product=instance)
        return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form,'existing_images':existing_images,'edit':True})
    def post(self,request,id,*args, **kwargs):
       
        try:
            instance = ProductVariant.objects.get(id=id)
        except ProductVariant.DoesNotExist as e:
            print(e)
        print(request.POST)
        existing_images = ProductImage.objects.filter(product=instance)
        form = ProductSimpleVairentForm(request.POST,instance=instance)
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        existing_images_id = request.POST.getlist('existing_ids')
        image_types = request.POST.getlist('image_types')
        deleted_ids = request.POST.getlist('deleted_ids')
        if len(orders) != len(primary) or len(orders) != len(image_types):
            form.add_error(None, 'Image Upload has some issue')
            return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form,'existing_images':existing_images,'edit':True})
        if form.is_valid():  
            try:
                with transaction.atomic():
                    form.save()
                try:
                    count = 0
                    acount = 0
                    for i in range(len(image_types)):
                        if image_types[i] == 'existing':
                            try:
                                
                                obj = ProductImage.objects.get(id=existing_images_id[count])
                                count +=1
                            except ProductImage.DoesNotExist as e:
                                print(e)
                            obj.display_order = orders[i]
                            obj.is_thumbnail = True if primary[i] == '1' else False 
                        else: 
                            img_obj = ProductImage(product=instance,display_order = orders[i],is_thumbnail = True if primary[i] == '1' else False,image=files[acount])
                            acount +=1
                            img_obj.save()
                            
                    for i in deleted_ids:
                        try:
                            obj = ProductImage.objects.get(id=i)
                            obj.delete()
                        except ProductImage.DoesNotExist as e:
                            print(e)
                    messages.success(request,'Update succsessfull')               
                    return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form,'existing_images':existing_images,'edit':True})   
                except Exception as e:
                    print(e)
                    print('here')
            except:
                pass
        return render(request,'c_admin/admin-products-interior-add-simple.html',{'form':form,'existing_images':existing_images,'edit':True})

class AdminProductVarientEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        try:
            instance = ProductVariant.objects.get(id=id)
        except ProductVariant.DoesNotExist as e:
            print(e)
        color_form = ColorForm()
        size_form = SizeForm()
        form = ProductSimpleVairentForm(instance=instance)
        if instance.color:
            try:
                color_form = ColorForm(instance=instance.color)
            except Color.DoesNotExist as e:
                print(e)
        elif instance.size:
            try:
                size_form = SizeForm(instance=instance.size)
            except Size.DoesNotExist as e:
                print(e)
        exsiting_images = ProductImage.objects.filter(product=instance)
                
        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
    
    
    def post(self,request,id,*args, **kwargs):
        try:
            instance = ProductVariant.objects.get(id=id)
        except ProductVariant.DoesNotExist as e:
            print(e)
        color_form = ColorForm()
        size_form = SizeForm()
        form = ProductSimpleVairentForm(instance=instance)
        if instance.color:
            try:
                color_form = ColorForm(instance=instance.color)
            except Color.DoesNotExist as e:
                print(e)
        elif instance.size:
            try:
                size_form = SizeForm(instance=instance.size)
            except Size.DoesNotExist as e:
                print(e)
        exsiting_images = ProductImage.objects.filter(product=instance)
                
        
        
        print(request.POST)
        print(request.FILES)
        
        # return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
        
        data = request.POST
        form = ProductSimpleVairentForm(request.POST,instance=instance)
        if request.POST.get('variant_type_variant-1') == 'Color':
            colorhex = request.POST.get('variant_color_code_variant-1') 
            color_name = request.POST.get('variant_color_variant-1')
            color_form = ColorForm(data={'hex':colorhex,'name':color_name},instance=instance.color)
         
            if ProductVariant.objects.filter(product=instance.product,color__name__iexact=color_name).exclude(id=instance.id).exists():
                        messages.error(request,'The Color Already added')
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
            try:
                with transaction.atomic():
                    if color_form.is_valid():
                        color = color_form.save()
                        response =  self.updating_data(request=request,form=form,instance=instance,color=color,color_form=color_form)
                        if response[0] == False:
                            return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':response[1],'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
                        elif response[0] == True:
                            messages.success(request,'update succsessfull')
                            return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
                    else:
                                    
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':response,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
            except Exception as e:
                 print("Error:", e)
                 messages.error(request, "Something went wrong. Please try again.")
                 return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
        else:
            try:
                with transaction.atomic():
                    size_form = SizeForm(data={
                        'name':request.POST.get('variant_size_variant-1'),
                        'sort_order':int(request.POST.get('variant_size_order_variant-1'))
                        
                    },instance=instance.size)
                    
                    if ProductVariant.objects.filter(product=instance.product,size__name__iexact=request.POST.get('size')).exclude(id=instance.product.id).exists():
                        messages.error(request,'The Size Already added')
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
                    if size_form.is_valid():
                        size_obj = size_form.save()
                        response = self.updating_data(request=request,form=form,instance=instance,size=size_obj,size_form=size_form)
                        if response[0] == False:
                            return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':response[1],'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
                        elif response[0] == True:
                            messages.success(request,'update succsessfull')
                            return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True}) 
                    else:
                        print(size_form.errors)
                        return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
            except Exception as e:
                 print("Error:", e)
                 messages.error(request, "Something went wrong. Please try again.")
                 return render(request,'c_admin/admin-products-interior-add-variants.html',{'form':form,'color_form':color_form,'size_form':size_form,'exsiting_images':exsiting_images,'edit':True})
            
            
    def updating_data(self,request,form,instance,color=None,size=None,color_form=None,size_form=None):
        
        
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        image_types = request.POST.getlist('image_types')
        deleted_ids = request.POST.getlist('deleted_ids')
        existing_images = request.POST.getlist('existing_images')
        if len(orders) != len(primary) or len(orders) != len(image_types):
            form.add_error(None, 'Image Upload has some issue')
            return [False,form]
        
        if form.is_valid():
            form.save()     
            try:
                count =0 
                file_count = 0
                for i in range(len(image_types)):
                    order = int(orders[i]) if orders[i] not in [None, ''] else (i + 1)
                    if image_types[i] =='existing':
                        try:
                            img_obj = ProductImage.objects.get(id=existing_images[count])
                            count+=1
                        except ProductImage.DoesNotExist as e:
                            print(e)
                        img_obj.display_order = order
                        img_obj.is_thumbnail = False if primary[i] == '0' else True
                        img_obj.save()
                    else:
                        img_obj = ProductImage(product=instance,display_order=order,is_thumbnail=True if primary[i] == '1' else False,image=files[file_count] )
                        file_count += 1
                        img_obj.save()
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong. Please try again.")
            
            return [True]
        
def redirect_to_add_varient(request,id):
    request.session['pending_product_add_id'] = id
    return redirect('cadmin:varient_or_not')


class AdminDecorationEdit(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        try:
            instance = Decoration.objects.get(id=id)
        except Decoration.DoesNotExist as e:
            print(e)
        exsiting_images = DecorationImages.objects.filter(product=instance)
        form = DecorationForm(instance=instance)
        return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'existing_images':exsiting_images,'edit':True})
    
    def post(self,request,id,*args, **kwargs):
        print(request.POST,request.FILES)
        try:
            instance = Decoration.objects.get(id=id)
        except Decoration.DoesNotExist as e:
            print(e)
        exsiting_images = DecorationImages.objects.filter(product=instance)
        form = DecorationForm(request.POST,instance=instance)
       
        print(request.POST)
        print(request.FILES)
        files = request.FILES.getlist('images')
        orders = request.POST.getlist('orders')
        primary = request.POST.getlist('primary')
        deleted_ids = request.POST.getlist('deleted_ids')
        seq_types = request.POST.getlist('seq_types')
        existing_ids = request.POST.getlist('existing_ids')
    
        if len(orders) != len(primary) or len(orders) != len(seq_types):
            form.add_error(None, 'Image Upload has some issue')
            return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'existing_images':exsiting_images,'edit':True})
        if form.is_valid():
            obj = form.save()
            
            try:
                count = 0
                acount = 0
                for i in range(len(seq_types)):
                    if seq_types[i] == 'existing':
                        try:
                            img_obj = DecorationImages.objects.get(id=existing_ids[count])
                        except DecorationImages.DoesNotExist as e:
                            print(e)
                        count += 1
                        img_obj.display_order = orders[i]
                        img_obj.is_thumbnail = True if primary[i] == '1' else False
                        img_obj.save()
                    else:
                        
                        img_obj = DecorationImages(product=instance,display_order=int(orders[i]),is_thumbnail=True if primary[i] == '1' else False,image=files[acount] )
                        
                        img_obj.save()
                        acount += 1
                for i in deleted_ids:
                    try:
                        img_obj = DecorationImages.objects.get(id=i)
                        print(i)
                        img_obj.delete()
                    except DecorationImages.DoesNotExist as e:
                        print(e)
                        
                
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong. Please try again.")
            
            return redirect('cadmin:decoration_manage')
        return render(request,'c_admin/admin-products-decorations-add.html',{'form':form,'existing_images':exsiting_images,'edit':True})