from django.db import models
import uuid
from django.utils import timezone
from django.db.models import F


from accounts.models import CustomUser
# from order.models import Order
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
    used_count = models.IntegerField(default=0,blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    def valid_token(self):
        if not self.is_active:
            return False
        if self.is_deleted:
            return False
        now = timezone.now()
        if not self.valid_from <= now <= self.valid_to:
            return False
        if not self.usage_limit > self.used_count:
            return False
            
        return True
        
    
    
    @classmethod
    def custom_objects(cls):
        return cls.objects.filter(is_deleted=False)
    
    @classmethod
    def total_working_codes(cls):
        now = timezone.now()
        print(now)
        print(cls.custom_objects().first().valid_from)
        return cls.custom_objects().filter(valid_from__lte=now,valid_to__gte=now,used_count__lt=F('usage_limit'))
    

        
        
        
    
    
class PromoCodeUsage(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
        )
    discount_given = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    promo_code = models.ForeignKey(
        PromoCode,on_delete=models.CASCADE
    )
    used_at = models.DateTimeField(
        auto_now=True
    )
    user = models.ForeignKey(
        CustomUser,on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.SET_NULL,
        null=True,      # ✅ REQUIRED
        blank=True
    )