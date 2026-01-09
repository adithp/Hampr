from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.edit import CreateView,DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import CustomUserCreationForm,EmailOrUsernameLogin,UserAddressForm
from core.decorators import otp_pending_verify
from .models import CustomUser,OTP,UserAddress
from .utils import otp_send_signup,otp_block_time_verify,password_reset_link,token_checker
from core.utils import FMT
from core.mixins import NeverCacheMixin,GuestOnlyMixin,OnlyForUsers



class UserSignupView(GuestOnlyMixin,CreateView):
    
    template_name = 'accounts/hampr_signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:otp_verify')
    
    def form_valid(self, form):
        user = form.save()
        otp_send_signup(self.request,user)
        response = super().form_valid(form)
        return response
    
    
@method_decorator(otp_pending_verify,name='dispatch')
class Otp_Verify_View(NeverCacheMixin,View):
    
    def get(self,request,*args, **kwargs):
        return render(request,'accounts/hampr_otp_verification.html')
    
    def post(self,request,*args,**kwargs):
        otp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + request.POST.get('otp4')
        user_id = request.session.get('otp_pending_user_id')
        user = CustomUser.objects.get(id=user_id)
        obj_otp = OTP.objects.filter(user=user_id).latest('created_at')
        now = timezone.now()
        obj_otp.attempts = obj_otp.attempts + 1
        obj_otp.save()
        if obj_otp.expires_at < now:
            return render(request,'accounts/hampr_otp_verification.html',{'error':'otp is expired resend one more time'})
        if obj_otp.attempts > 5:
            return render(request,'accounts/hampr_otp_verification.html',{'error':'otp limit exceded resend otp one more time'})
        if obj_otp.otp_code != otp:
            return render(request,'accounts/hampr_otp_verification.html',{'error':'otp invalid'})
        user.email_verified = True      
        user.save()
        del request.session['otp_pending']
        del request.session['otp_pending_user_id']
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        obj_otp.delete()
        
        return redirect(reverse_lazy('core:landing_page'))
 


class Otp_Resend(View):
    def get(self,request,*args, **kwargs):
        user_id = self.request.session.get('otp_pending_user_id')
        if not user_id:
            return JsonResponse({
                "success":False,"message":'user not found '  
            },status=429)
        
        
        
        out = otp_block_time_verify(self.request)
        if not out is True:
            return  JsonResponse({
                "success":False,"message":out  
            },status=429)
        count = request.session.get('otp_send_count',{})
        if count and count >= 5:
            now = timezone.now()
            block_time = now + timedelta(hours=2)
            request.session['block_time'] = block_time.strftime(FMT)
            return JsonResponse({
                "success":False,"message":'otp limit reached you can send otp only after 2 hour'  
            },status=429)
        else:
            user = CustomUser.objects.get(id=user_id)
            otp_send_signup(self.request,user)
            return  JsonResponse({
                "success":True,"message":'otp send succsesfull'  
            })
 
 
class BackButtonOtp(View):
    def get(self,req,*args, **kwargs):
        user_id = self.request.session.get('otp_pending_user_id')  
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'succses':True})


class CustomLoginView(NeverCacheMixin,GuestOnlyMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request,'accounts/hampr_login.html')
    
    def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(Q(username=identifier)| Q(email=identifier))
        except CustomUser.DoesNotExist:
            messages.error(request,"Invalid Username")
            return redirect(reverse_lazy('accounts:login'))
        if user.has_usable_password():
            if not user.check_password(password):
                messages.error(request, "password invalid")
                return redirect(reverse_lazy('accounts:login'))
        else:
            messages.error(request, "This account was created with Google. Please login using Google.")
            return redirect(reverse_lazy('accounts:login'))
        
        if not user.is_active:
            messages.error(request,"Contact admin user blocked by admin")
            return redirect(reverse_lazy('accounts:login'))
        if  user.is_staff or user.is_staff :
            messages.error(request,"this page is not access for admin")
            return redirect(reverse_lazy('accounts:login'))
        
        if not user.email_verified:
            out = otp_block_time_verify(self.request)
            if not out is True:
                messages.error(request,f"your account not verified {out}")
                return redirect(reverse_lazy('accounts:login'))
            count = request.session.get('otp_send_count',{})
            if count and count >= 5:
                now = timezone.now()
                block_time = now + timedelta(hours=2)
                request.session['block_time'] = block_time.strftime(FMT)
            obj = otp_send_signup(self.request,user)
            return redirect(reverse_lazy('accounts:otp_verify'))
        user.backend = 'django.contrib.auth.backends.ModelBackend'  
        login(request,user)
        return redirect(reverse_lazy('core:landing_page'))
    
    
@method_decorator(never_cache,name='dispatch')
class ResetPasswordLinkSend(View):
    
    def get(self,request,*args, **kwargs):
        return render(request,'accounts/hampr_forgot_password.html')
    
    def post(self,request,*args, **kwargs):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request,'Email id not found')
            return redirect('accounts:reset_link')
        if not user.has_usable_password():
            messages.error(request,'user created through google social login cannot set password')
            return redirect('accounts:reset_link')
        already = cache.get(f'reset:{user.id}')
        
        if already:
            messages.error(request,'Reset link already sent. Please wait 5 minutes before trying again')
            return redirect('accounts:reset_link')
        
        password_reset_link(user)
        cache.set(f"reset:{user.id}",1,1800)
        messages.success(request,'Succsesfully send password reset link to your email')
        return redirect('accounts:reset_link')
        
        
@method_decorator(never_cache,name='dispatch')
class ResetPassword(View):
    
    def get(self,request,*args, **kwargs):
        raw_token = kwargs.get('id')
        output = token_checker(raw_token)
        if not output:
            return render(request,'accounts/invalidlink.html')
        return render(request,'accounts/hampr_reset_password.html')
    
    def post(self,request,*args, **kwargs):
        raw_token = kwargs.get('id')
        output = token_checker(raw_token)
        if not output:
            return render(request,'accounts/invalidlink.html')
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return render(request, 'accounts/hampr_reset_password.html', {
            'error': 'Password and Confirm Password do not match'
        })
        
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'accounts/hampr_reset_password.html',{'errors':e.messages})
        
        output.user.set_password(password)
        output.user.save()
        output.delete()
        return render(request,'accounts/password_reset_succsesfull.html')
            

def not_active_error(req):
    return render(req,'accounts/user_inactive.html')





    
class ProfilePageView(LoginRequiredMixin,OnlyForUsers,View):
    def get(self,request,*args, **kwargs):
        # user_id = request.user.id
        # try:
        #     user = CustomUser.objects.get(id=user_id)
        # except CustomUser.DoesNotExist as e:
        #     print(e)
        form = UserAddressForm()
        address = UserAddress.objects.filter(user=request.user)
        has_default_address = UserAddress.objects.filter(user=request.user,is_default=True).exists()
        return render(request,'accounts/account.html',{'form':form,'address':address,'has_default_address':has_default_address})
    
    
class ProfilePictureUpdate(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        image = request.FILES.get('image','')
        if image:
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']

            if image.content_type not in allowed_types:
                messages.error(request,'Image Type Jpg png and Webp Only Allowed')
                return redirect('accounts:user_profile')
            user_id = request.user.id
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist as e:
                print(e)
            user.profile_picture = image
            user.save()
        return redirect('accounts:user_profile')

class AddAddressView(LoginRequiredMixin,OnlyForUsers,View):
    def post(self,request,*args, **kwargs):
        form = UserAddressForm(request.POST)
        form.usert = request.user
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

        
            
            return redirect('accounts:user_profile',)
        address = UserAddress.objects.filter(user=request.user)
        return render(request,'accounts/account.html',{'form':form,'address':address})
    
class EditAddressView(LoginRequiredMixin,OnlyForUsers,View):
    def post(self,request,id,*args, **kwargs):
        try:
            instance = UserAddress.objects.get(id=id)
        except UserAddress.DoesNotExist as e:
            print(e)
        form = UserAddressForm(self.request.POST,instance=instance)
        form.usert = request.user
        if form.is_valid():
            form.save()
            return redirect('accounts:user_profile',)
        address = UserAddress.objects.filter(user=request.user)
        return render(request,'accounts/account.html',{'form':form,'address':address})
    

class DeleteAddressView(DeleteView):
    model = UserAddress
    success_url = reverse_lazy("accounts:user_profile")
    
    