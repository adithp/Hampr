from django.db import models
import uuid


from autoslug import AutoSlugField


class BoxType(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    name =  models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class BoxCategory(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    box_type = models.ForeignKey(BoxType,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from="name",unique=True)
    
    def __str__(self):
        return self.name
    
    
class BoxCategoryImage(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=True)
    box_category = models.ForeignKey(BoxCategory,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    display_order = models.IntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='category_images/')
    is_primary = models.BooleanField(default=False)
    
    
    
    
class HamperBox(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    category = models.ForeignKey(BoxCategory,on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=40)
    slug = AutoSlugField(populate_from='name',unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class BoxSize(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    hamper_box = models.ForeignKey(HamperBox, on_delete=models.CASCADE, related_name='sizes')
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    width = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    depth = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    cost = models.DecimalField(max_digits=10, decimal_places=2)      
    price = models.DecimalField(max_digits=10, decimal_places=2)     
    stock = models.IntegerField()
    size_label = models.CharField(max_length=50, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('hamper_box', 'size_label')

    
class BoxImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField(null=True,blank=True)
    image = models.ImageField(upload_to='box_images/')
    is_thumbnail = models.BooleanField(default=False)
    box_id = models.ForeignKey(HamperBox,on_delete=models.CASCADE)
    
    
class Color(models.Model):
    name = models.CharField(max_length=64)
    hex = models.CharField(max_length=7, blank=True, null=True)
    
    
class Size(models.Model):
    name = models.CharField(max_length=32, unique=True)
    sort_order = models.PositiveSmallIntegerField(default=0) 
    

    
    
class ProductCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True, related_name='children')
    slug = AutoSlugField(populate_from='name',unique=True)
    
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    avg_rating = models.DecimalField(blank=True,null=True,max_digits=4,decimal_places=2)
    brand = models.CharField(max_length=30)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name',unique=True)
    total_reviews = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    # sku = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    is_default = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    width = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    depth = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ProductImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField()
    image = models.ImageField(upload_to='product_image/')
    is_thumbnail = models.BooleanField(default=False)
    product = models.ForeignKey(ProductVariant,on_delete=models.CASCADE) 
    
    
    
class Decoration(models.Model):
    name = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    width = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    depth = models.DecimalField(max_digits=5, decimal_places=2, help_text="unit is cm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name',unique=True)
    is_outside = models.BooleanField(default=False)
    is_inside = models.BooleanField(default=False)


class DecorationImages(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField()
    image = models.ImageField(upload_to='decoration_image/')
    is_thumbnail = models.BooleanField(default=False)
    product = models.ForeignKey(Decoration,on_delete=models.CASCADE) 
    
    
    
    
    
    
    
    