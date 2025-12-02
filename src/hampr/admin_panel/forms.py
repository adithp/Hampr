from catalog.models import BoxCategory,BoxType,HamperBox
from django import forms
import re
from django.core.exceptions import ValidationError


class HamperBoxForm(forms.ModelForm):
    
    
    class Meta():
        model = HamperBox
        fields = '__all__'
        
        
class BoxTypeForm(forms.ModelForm):
 
    class Meta():
        model = BoxType
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'type':'text','class':'form-control','id':'typeName','placeholder':"e.g., Standard Box, Basket, Wooden Crate",'maxlength':"50",'required':True,'oninput':"validateInput(this)"}),
            'description':forms.Textarea(attrs={'class':"form-control",'id':"typeDescription",'row':'4', 'placeholder':"Describe this box type...",'maxlength':'200','oninput':"updateCharCount(this)"}),
            'is_active':forms.CheckboxInput(attrs={'class':"form-check-input",'type':'checkbox','id':"typeStatus",'checked':True})
        }
        

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Box Name Is Required")
        
        if len(name) < 3:
            raise ValidationError("Box Length Must be under 3 characters")
        
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Box name must contain only alphabets and spaces")
        if BoxType.objects.filter(name__iexact=name).exists():
            raise ValidationError("This box name already exists")
        
        
        return name
    
class BoxCategoryAdd(forms.ModelForm):
    

    
    class Meta:
        model = BoxCategory
        fields = '__all__'
        widgets = {
            'box_type':forms.Select(attrs={
                'class': 'form-select',
                'id': 'boxType',
                'required': True,
                'onchange': 'validateInput(this)',
            }),
            'name':forms.TextInput(attrs={'type':'text','class':'form-control','id':'categoryName','placeholder':"e.g., Birthday, Wedding",'maxlength':"50",'required':True,'oninput':"validateInput(this)"}),
            'description':forms.Textarea(attrs={'class':"form-control",'id':"categoryDescription",'row':'4', 'placeholder':"Describe this category...",'maxlength':'200','oninput':"updateCharCount(this)"}),
            'is_active':forms.CheckboxInput(attrs={'class':"form-check-input",'type':'checkbox','id':"categoryStatus",'checked':True})
        }
        
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['box_type'].empty_label = "Select Box Type"
        
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Box Name Is Required")
        
        if len(name) < 3:
            raise ValidationError("Box Length Must be under 3 characters")
        
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Box name must contain only alphabets and spaces")
        if BoxType.objects.filter(name__iexact=name).exists():
            raise ValidationError("This box name already exists")
        
        
        return name
    