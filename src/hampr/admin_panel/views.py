from django.shortcuts import render
from django.views.generic import TemplateView
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


from .mixins import StaffRequiredMixin,LoginInRedirectMixin
from core.mixins import NeverCacheMixin
from .forms import HamperBoxForm,BoxTypeForm,BoxCategoryAdd,BoxSizeForm
from catalog.models import BoxCategory,BoxType,HamperBox,BoxCategoryImage



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
        return redirect('cadmin:user_management')
    
    
    
class AdminProductsMainPage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products.html'
    
    
class AdminBoxProductsMainPage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-boxes.html'
    
class AdminBoxTypeManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-box-types.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        box_types = BoxType.objects.all()
        context['box_types'] = box_types
        return context
    
class AdminBoxCategoryManage(NeverCacheMixin,StaffRequiredMixin,TemplateView):
    template_name = 'c_admin/admin-products-box-categories.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        box_categories = BoxCategory.objects.all()
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
            messages.success(request, "Box Type added successfully!")
            return redirect('cadmin:box_type_manage')
        else:
            return render(request,'c_admin/admin-products-box-types-add.html',{'form':form})


class AdminBoxCategoryItemAdd(NeverCacheMixin,StaffRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        form = BoxCategoryAdd()
        return render(request,'c_admin/admin-products-box-categories-add.html',{'form':form,})
    
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
                        
                        
                    
                messages.success(request, "Box Type added successfully!")
                return redirect('cadmin:box_category_add')
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
        request.session.get('product_add_first_stage',{})
        
        form = BoxSizeForm()
        return render(request,'c_admin/admin-products-boxes-add-step2.html',{'form':form,})