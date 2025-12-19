from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator


from .models import BoxType,BoxCategory,HamperBox,BoxImage,BoxSize

class BoxListView(View):
    def get(self,request,*args, **kwargs):
        data = []
        box_types = BoxType.objects.all()
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
        for i in range(len(boxes_all)):
            
            data.append({
                'box':boxes_all[i],
                'image':BoxImage.objects.filter(box_id=boxes_all[i],is_thumbnail=True).first(),
                'box_vareint':BoxSize.objects.filter(hamper_box=boxes_all[i]),
                'size':BoxSize.objects.filter(hamper_box=boxes_all[i]).first(),
                
                
            })
        return render(request,'catalog/shop-boxes.html',{'box_types':box_types,'box_categories':box_categories,'boxes':data,'size_list':size_list,'selected_boxes': selected_boxes,'selected_categories':selected_categories,'selected_sizes':selected_sizes,'total_page_num':total_page_num,'count':i+1})
    
    
def box_search_suggestions(request):
    q = request.GET.get('suggest','').strip()
    
    if len(q) > 1:
        
        boxes = HamperBox.objects.filter(name__icontains=q).order_by('-created_at').values('id','name')[:6]
            
        return JsonResponse({"results":list(boxes)})
    
    return JsonResponse({"results": []})


        
            