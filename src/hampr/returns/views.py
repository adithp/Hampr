from django.shortcuts import render,redirect
from django.views import View
from .forms import OrderReturnForm
from .models import ReturnImage,ReturnVideo,OrderReturn
from django.contrib import messages
from django.http import HttpResponse

from order.models import Order
from order.services import send_order_email
# Create your views here.


class ReturnPage(View):
    def get(self,request,id,*args, **kwargs):
        form = OrderReturnForm()
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist as e:
            print(e)
            
        if order.user != request.user:
            return HttpResponse("Only Access For The User Who Ordered This")
        if OrderReturn.objects.filter(order=order).exists():
            messages.warning(request,"already return submitted")
            return redirect('accounts:user_profile')
        
        
        return render(request,'return/return_create.html',{'form':form})
    
    
    def post(self,request,id,*args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist as e:
            print(e)
            
        if order.user != request.user:
            return HttpResponse("Only Access For The User Who Ordered This")
        valid_content_types = [
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/jpg',
        ]
        valid_content_types_video = [
        'video/mp4',
        'video/webm',
        'video/ogg',
        'video/quicktime',  # .mov
    ]
        form = OrderReturnForm(request.POST)
        images = request.FILES.getlist('images')
         
        for i in images:
            content_type = i.content_type
            if content_type not in valid_content_types:
                messages.error(request, "Unsupported file type. Allowed types: JPEG, PNG, WEBP." )
                return render(request,'return/return_create.html',{'form':form})
        videos = request.FILES.getlist('videos')
        for i in videos:
            content_type = i.content_type
            if content_type not in valid_content_types_video:
                messages.error(request,"Unsupported file type. Allowed Videos Only MP4,WEBM,OGG,QUICKTIME")
                return render(request,'return/return_create.html',{'form':form})
        form.instance.order = order
        form.instance.user = request.user
        if form.is_valid():
            
            return_obj = form.save()
            for i in images:
                obj = ReturnImage(image=i,return_request=return_obj)
                obj.save()
            for i in videos:
                obj = ReturnVideo(video=i,return_request=return_obj)
                obj.save()
            messages.success(request,"return Request Succsessfully Completed")
            
                
                
        return render(request,'return/return_create.html',{'form':form})