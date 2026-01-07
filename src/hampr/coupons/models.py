from django.db import models
import uuid


from accounts.models import CustomUser
# Create your models here.


class PromoCode(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENT', 'Percentage'),
        ('AMOUNT', 'Flat amount')
        ]
    
    
    code = models.CharField(
        max_length=12,
    )
    created_at = models.DateTimeField(
        auto_now=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    descroption = models.TextField(
        null=True,blank=True
    )
    discount_type = models.CharField(
        choices=DISCOUNT_TYPE_CHOICES,
        max_length=10
    )
    discount_value = models.DecimalField(
        max_digits=10,decimal_places=2
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    is_active = models.BooleanField(
        default=True
    )
    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_deleted = models.BooleanField(
        default=False
    )
    usage_limit = models.IntegerField()
    used_count = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    @classmethod
    def custom_objects(cls):
        return cls.objects.filter(is_deleted=False)
    
    
# class PromoCodeUsage(models.Model):
#     id = models.UUIDField(
#         default=uuid.uuid4,
#         primary_key=True,
#         editable=False
#         )
#     discount_given = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#     promo_code = models.ForeignKey(
#         PromoCode,on_delete=models.CASCADE
#     )
#     used_at = models.DateTimeField(
#         auto_now=True
#     )
#     user = models.ForeignKey(
#         CustomUser,on_delete=models.SET_NULL
#     )
#     order = models.ForeignKey()