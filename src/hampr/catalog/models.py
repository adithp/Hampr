from django.db import models
import uuid


from autoslug import AutoSlugField


class BoxType(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    name =  models.CharField(max_length=20)
    
    
class BoxCategory(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    box_type = models.ForeignKey(BoxType,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from="name",unique=True)
    
    
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
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    depth = models.DecimalField(help_text="unit is cm",max_digits=5,decimal_places=2)
    description = models.TextField()
    height = models.DecimalField(help_text="unit is cm",max_digits=5,decimal_places=2)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    slug = AutoSlugField(populate_from='name',unique=True)
    stock = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)
    width = models.DecimalField(help_text="unit in cm",max_digits=5,decimal_places=2)
    
    
    
    
    
    
    