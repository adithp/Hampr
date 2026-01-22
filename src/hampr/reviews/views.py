from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
import json

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .forms import ProductReviewForm
from .models import ProductReviews, BoxReviews,DecorationReviews,ReviewImage
from catalog.models import HamperBox,Product,Decoration






ITEM_TYPE_MODEL_MAP = {
    "box": BoxReviews,
    "product": ProductReviews,
    "decoration": DecorationReviews,
}
class CreateReview(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        ALLOWED_CONTENT_TYPES = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }
        print(request.POST)
        images = request.FILES.getlist('images')
        
        for image in images:
            if image.content_type not in ALLOWED_CONTENT_TYPES:
                return JsonResponse({"error": "Invalid Image  type"}, status=400)
        
        form = ProductReviewForm(request.POST)

        item_type = request.POST.get("item_type")
        item_id = request.POST.get("item_id")

        if item_type not in ITEM_TYPE_MODEL_MAP:
            return JsonResponse({"error": "Invalid item type"}, status=400)

        model = ITEM_TYPE_MODEL_MAP[item_type]
        if item_type == 'box':
            try:
                item_object = HamperBox.objects.get(id=item_id)
            except model.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        elif item_type == 'product':
            try:
                item_object = Product.objects.get(id=item_id)
            except model.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        elif item_type == 'decoration':
            try:
                item_object = Decoration.objects.get(id=item_id)
            except model.DoesNotExist:
                return JsonResponse({"error": "Item not found"}, status=404)
        if form.is_valid():
            if item_type == 'box':
                if model.objects.filter(user=request.user,box=item_object).exists():
                    return JsonResponse({"error": "already have written review"}, status=404)
                    
                obj = model.objects.create(
                user=request.user,
                rating=form.cleaned_data["rating"],
                review_text=form.cleaned_data.get("review_text"),
                box=item_object
            )
            elif item_type == 'product':
                if model.objects.filter(user=request.user,product=item_object).exists():
                        return JsonResponse({"error": "already have written review"}, status=404)
                obj = model.objects.create(
                user=request.user,
                rating=form.cleaned_data["rating"],
                review_text=form.cleaned_data.get("review_text"),
                product=item_object
            )
            elif item_type == 'decoration':
                if model.objects.filter(user=request.user,decoration=item_object).exists():
                        return JsonResponse({"error": "already have written review"}, status=404)
                obj = model.objects.create(
                    user=request.user,
                    rating=form.cleaned_data["rating"],
                    review_text=form.cleaned_data.get("review_text"),
                    decoration=item_object
                )
                
            img_objs = [
            ReviewImage(
                image=i,
                content_type= ContentType.objects.get_for_model(obj),
                object_id=obj.id,
            ) for i in images
        ]
            ReviewImage.objects.bulk_create(img_objs)
            
                
            
            
           
                    
            
                

            return JsonResponse({"success": True})
        print('error' , form)
        return JsonResponse({"errors": form.errors}, status=400)
    
    
class DeleteReviewModel(DeleteView):
    def post(self,request,id,*args, **kwargs):
        data = json.loads(request.body)
        item_type = data.get('item_type')
        if item_type == 'box':
            try:
                boxReview = BoxReviews.objects.get(id=id)
            except BoxReviews.DoesNotExist as e:
                return JsonResponse(
                {'success': False, 'message': 'review not found'},
                status=403
            )
            if boxReview.user != request.user:
                return JsonResponse(
                {'success': False, 'message': 'Unauthorized'},
                status=403
            )
            boxReview.delete()
            return JsonResponse({
            'success': True,
            'message': 'Review deleted successfully'
                })
        elif item_type == 'decoration':
            try:
                decorationReview = DecorationReviews.objects.get(id=id)
            except DecorationReviews.DoesNotExist as e:
                return JsonResponse(
                {'success': False, 'message': 'review not found'},
                status=403
            )
            if decorationReview.user != request.user:
                return JsonResponse(
                {'success': False, 'message': 'Unauthorized'},
                status=403
            )
            decorationReview.delete()
            return JsonResponse({
            'success': True,
            'message': 'Review deleted successfully'
                })
            
        elif item_type == 'product':
            try:
                productReview = ProductReviews.objects.get(id=id)
            except ProductReviews.DoesNotExist as e:
                return JsonResponse(
                {'success': False, 'message': 'review not found'},
                status=403
            )
            if productReview.user != request.user:
                return JsonResponse(
                {'success': False, 'message': 'Unauthorized'},
                status=403
            )
            productReview.delete()
            return JsonResponse({
            'success': True,
            'message': 'Review deleted successfully'
                })
        