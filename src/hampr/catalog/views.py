from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


from .models import BoxType,BoxCategory,HamperBox,BoxImage,BoxSize

class BoxListView(View):
    def get(self,request,*args, **kwargs):
        data = []
        box_types = BoxType.objects.all()
        boxes_all = HamperBox.objects.all()
        selected_boxes = request.GET.getlist('box')
        print(selected_boxes)
        q = request.GET.get('search')
        if selected_boxes:
            boxes_all = HamperBox.objects.filter(category__box_type__name__in=selected_boxes)
        if q:
            boxes_all = boxes_all.filter(name__icontains=q)
        box_categories = BoxCategory.objects.all()
        
        
        data = []
        size_list = BoxSize._meta.get_field('size_label').choices
        for i in range(len(boxes_all)):
            
            data.append({
                'box':boxes_all[i],
                'image':BoxImage.objects.filter(box_id=boxes_all[i],is_thumbnail=True).first(),
                'box_vareint':BoxSize.objects.filter(hamper_box=boxes_all[i]),
                'size':BoxSize.objects.filter(hamper_box=boxes_all[i]).first(),
                
                
            })
        return render(request,'catalog/shop-boxes.html',{'box_types':box_types,'box_categories':box_categories,'boxes':data,'size_list':size_list,'selected_boxes': selected_boxes, })
    
    
def box_search_suggestions(request):
    q = request.GET.get('suggest','').strip()
    
    if len(q) > 1:
        
        boxes = HamperBox.objects.filter(name__icontains=q).order_by('-created_at').values('id','name')[:6]
            
        return JsonResponse({"results":list(boxes)})
    
    return JsonResponse({"results": []})


        
            