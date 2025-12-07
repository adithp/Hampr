from catalog.models import BoxCategory,BoxType,HamperBox,BoxSize,ProductCategory,Product,ProductVariant,Color,Size,Decoration
from django import forms
import re
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

class HamperBoxForm(forms.ModelForm):
    

    class Meta():
        model = HamperBox
        fields = '__all__'
        widgets = {
            'category':forms.Select(attrs={
                'class':'form-select',
                'id':'boxCategory',
                'required':True,
            }),
            'name':forms.TextInput(attrs={
                'type':'text',
                'class':'form-control',
                'id':'boxName',
                'placeholder':"e.g., Classic Kraft Box, Woven Basket",
                'maxlength':'40',
                'required':True,
                'oninput':"updateCharCount(this, 'nameCount')"
                
            }),
            'description':forms.Textarea(attrs={
                'class':"form-control",
                'id':"boxDescription",
                'rows':'5',
                'placeholder':"Describe materials, features, durability...",
                'maxlength':'1000',
                'oninput':"updateCharCount(this, 'descCount')"
                
            }),
            'is_active':forms.CheckboxInput(attrs={
                'class':"form-check-input",
                'type':"checkbox",
                'id':"activeStatus"
                
            })
        }
        
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select box type category'
        
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
    
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError("Box Name Is Required")
        
        if len(description) < 20:
            raise ValidationError("Box Length Must be under 20 characters")
        if description.isdigit():
            raise ValidationError("Must Conatin Alphabets")

        return description
    

    
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
            raise ValidationError("Box category  Name Is Required")
        
        if len(name) < 3:
            raise ValidationError("Box category Length Must be under 3 characters")
        
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Box name must contain only alphabets and spaces")
        if BoxCategory.objects.filter(name__iexact=name).exists():
            raise ValidationError("This box category name already exists")
        
        return name
    
    
class BoxSizeForm(forms.ModelForm):
    

    class Meta:
        model = BoxSize
        fields = ['height','width','depth','cost','price','stock','size_label','is_active']
        
        widgets = {
            'size_label':forms.Select(attrs={
                'class':'form-select size-select',
                'onchange':"updateSizeLabel(1, this)",
                
            }),
            'height':forms.TextInput(attrs={
                'type':'number',
                'class':'form-control',
                'placeholder':"Height",
                'required':True,
                'oninput':"calcVolume(1)"
                
            }),
            'width':forms.TextInput(attrs={
                'type':'number',
                'class':'form-control',
                'placeholder':"Width",
                'required':True,
                'oninput':"calcVolume(1)"
            }),
            'depth':forms.TextInput(attrs={
                'type':'number',
                'class':'form-control',
                'placeholder':"Depth",
                'required':True,
                'oninput':"calcVolume(1)"
            }),
            'cost':forms.TextInput(attrs={
                'type':'number',
                'class':"form-control cost-price",
                'placeholder':"0.00",
                'required':True,
                'oninput':"calcProfit(1)"
                
            }),
            'price':forms.TextInput(attrs={
                'type':'number',
                'class':"form-control selling-price",
                'placeholder':"0.00",
                'required':True,
                'oninput':"calcProfit(1)"
            }),
            'stock':forms.TextInput(attrs={
                'type':'number',
                'class':'form-control',
                'placeholder':'0',
                'required':True
            }),
            'is_active':forms.CheckboxInput(attrs={
                'class':'form-check-input',
                'type':'checkbox',
                'checked':True
            })
            
        
        
        
        
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size_label'].choices = [
            choice for choice in self.fields['size_label'].choices if choice[0] != ''
        ]
    def clean_height(self):
        height = self.cleaned_data.get('height')
        
        if float(height) < 0:
            raise ValidationError('height must be greater than 0 ')
        
        return height
    
    def clean_width(self):
        width = self.cleaned_data.get('width')
        
        if float(width) < 0:
            raise ValidationError('width must be greater than 0 ')
        
        return width
    
    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        
        if float(depth) < 0:
            raise ValidationError('depth must be greater than 0 ')
        
        return depth
    
    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if float(cost) < 0:
            raise ValidationError('cost must be greater than 0 ')
        
        return cost
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if int(stock) < 0:
            raise ValidationError('stock must be greater than 0 ')
        
        return stock

        

class ProductCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductCategory
        fields = '__all__'
        widgets = {
            
            'name':forms.TextInput(attrs={'type':'text','class':'form-control','id':'categoryName','placeholder':"e.g., Dress, Electronics",'maxlength':"50",'required':True,'oninput':"validateInput(this)"}),
            'description':forms.Textarea(attrs={'class':"form-control",'id':"categoryDescription",'row':'4', 'placeholder':"Describe this category...",'maxlength':'200','oninput':"updateCharCount(this)"}),
            'is_active':forms.CheckboxInput(attrs={'class':"form-check-input",'type':'checkbox','id':"categoryStatus",'checked':True})
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Product Category Name Is Required")
        
        if len(name) < 3:
            raise ValidationError("Product Category Length Must be under 3 characters")
        
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Product Category name must contain only alphabets and spaces")
        if ProductCategory.objects.filter(name__iexact=name).exists():
            raise ValidationError("This product category already exists")
        
        return name
        
        
class ProductForm(forms.ModelForm):
    


    
    class Meta:
        model = Product
        fields = ['brand','category','description','is_featured','name']
        widgets = {
            'name':forms.TextInput(attrs={
                'type':"text",
                'class':"form-control",
                'id':"productName",
                'placeholder':"e.g. Swiss Dark Chocolate",
                'required':True,
                'oninput':"updatePreview()"
                
            }),
            'brand':forms.TextInput(attrs={
                'type':"text",
                'class':"form-control",
                'id':"productBrand",
                'placeholder':"e.g. Lindt",
                'required':True,
            }),
            'description':forms.Textarea(attrs={
                'class':"form-control",
                'id':"productDescription",
                'placeholder':"Enter product details, ingredients, or benefits...",
            }),
            'is_featured':forms.CheckboxInput(attrs={
                'class':"form-check-input",
                'type':"checkbox",
                'id':"productFeatured"
            })
        }    



    def clean_brand(self):
        brand = self.cleaned_data.get('brand')
        
        if not brand:
            raise ValidationError("brand Name Is Required")
        
        if len(brand) < 3:
            raise ValidationError("brand Length Must be under 3 characters")
        
        if not re.match(r'^[A-Za-z1-9]+$', brand):
            raise ValidationError("Product name must contain only alphabets and spaces and numbers")
     
        
        return brand
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError("Description is mandatory")
        
        if len(description) < 30:
            raise ValidationError("description 30 characters is mandatory")
        
        if description.isdigit():
            raise ValidationError("description is not allowed only numbers")
        
        return description
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Product Name Is Required")
        
        if len(name) < 3:
            raise ValidationError("Product Length Must be under 3 characters")
        
        if name.isdigit():
            raise ValidationError("name is not allowed only numbers")
        return name
        
        
class ProductSimpleVairentForm(forms.ModelForm):
    
    class Meta:
        model = ProductVariant
        fields = ['cost','price','stock','width','height','depth']
        
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        
        if float(height) < 0:
            raise ValidationError('height must be greater than 0 ')
        
        return height
    
    def clean_width(self):
        width = self.cleaned_data.get('width')
        
        if float(width) < 0:
            raise ValidationError('width must be greater than 0 ')
        
        return width
    
    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        
        if float(depth) < 0:
            raise ValidationError('depth must be greater than 0 ')
        
        return depth
    
    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if float(cost) < 0:
            raise ValidationError('cost must be greater than 0 ')
        
        return cost
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if int(stock) < 0:
            raise ValidationError('stock must be greater than 0 ')
        if not float(stock).is_integer():
            raise ValidationError('Stock Must Be Whole Number')
        return stock
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if float(price) < 0:
            raise ValidationError('price must be greater than 0 ')
        
        return price
    
    
class ColorForm(forms.ModelForm):
    
    class Meta:
        model = Color
        fields = '__all__'

    def clean_hex(self):
        hex_value = self.cleaned_data['hex']
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_value):
            raise forms.ValidationError("Invalid hex color code")
        return hex_value

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r"^[A-Za-z][A-Za-z\s-]*[A-Za-z]$"
, name):
            raise forms.ValidationError("Color name may only contain letters, spaces, or hyphens.")
        return name
    
    
class SizeForm(forms.ModelForm):
    
    class Meta:
        model = Size
        fields = '__all__'
        
        
    def clean_name(self):
        name = self.cleaned_data['name']
        
        if not re.match(r"^[A-Za-z][A-Za-z\s-]*[A-Za-z]$"
, name):
            raise forms.ValidationError("Size name may only contain letters, spaces, or hyphens.")
        
        return name
    
    def clean_sort_order(self):
        sort_order = self.cleaned_data['sort_order']
        
        if not sort_order:
            raise forms.ValidationError('mandatory field')
        
        if sort_order < 0:
            raise forms.ValidationError('must be whole value')
        
        
        return sort_order
    
class DecorationForm(forms.ModelForm):
    
    class Meta:
        model = Decoration
        fields = ['name','height','width','depth','cost','price','stock','is_active','description','is_outside','is_inside']
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r"^[A-Za-z][A-Za-z\s-]*[A-Za-z]$"
, name):
            raise forms.ValidationError("Decorater name may only contain letters, spaces, or hyphens.")
        return name
    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if float(cost) < 0:
            raise ValidationError('cost must be greater than 0 ')
        
        return cost
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if int(stock) < 0:
            raise ValidationError('stock must be greater than 0 ')
        if not float(stock).is_integer():
            raise ValidationError('Stock Must Be Whole Number')
        return stock
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if float(price) < 0:
            raise ValidationError('price must be greater than 0 ')
        
        return price
    def clean_height(self):
        height = self.cleaned_data.get('height')
        
        if float(height) < 0:
            raise ValidationError('height must be greater than 0 ')
        
        return height
    
    def clean_width(self):
        width = self.cleaned_data.get('width')
        
        if float(width) < 0:
            raise ValidationError('width must be greater than 0 ')
        
        return width
    
    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        
        if float(depth) < 0:
            raise ValidationError('depth must be greater than 0 ')
        
        return depth