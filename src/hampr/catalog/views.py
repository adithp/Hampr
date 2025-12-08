from django.shortcuts import render
from django.views import View


from .models import BoxType,BoxCategory,HamperBox,BoxImage,BoxSize

class BoxListView(View):
    def get(self,request,*args, **kwargs):
        data = []
        box_types = BoxType.objects.all()
        box_categories = BoxCategory.objects.all()
        boxes_all = HamperBox.objects.all()
        data = []
        size_list = BoxSize._meta.get_field('size_label').choices
        for i in range(len(boxes_all)):
            
            data.append({
                'box':boxes_all[i],
                'image':BoxImage.objects.filter(box_id=boxes_all[i],is_thumbnail=True).first(),
                'box_vareint':BoxSize.objects.filter(hamper_box=boxes_all[i]),
                'size':BoxSize.objects.filter(hamper_box=boxes_all[i]).first()
                
            })
        return render(request,'catalog/shop-boxes.html',{'box_types':box_types,'box_categories':box_categories,'boxes':data,'size_list':size_list})