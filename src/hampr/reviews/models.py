from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


from catalog.models import Product,HamperBox,Decoration



class ProductReviews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_reviews')
    rating = models.PositiveIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    review_text = models.CharField(max_length=255,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class BoxReviews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    box = models.ForeignKey(HamperBox,on_delete=models.CASCADE,related_name='box_reviews')
    rating = models.PositiveIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    review_text = models.CharField(max_length=255,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
class DecorationReviews(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    decoration = models.ForeignKey(Decoration,on_delete=models.CASCADE,related_name='decoration_reviews')
    rating = models.PositiveIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    review_text = models.CharField(max_length=255,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    

class ReviewImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='review_images/',)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    review = GenericForeignKey("content_type", "object_id")