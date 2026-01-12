from django.db import models
import uuid
from django.conf import settings

from django.core.validators import MinValueValidator,MaxValueValidator
from catalog.models import ProductVariant,HamperBox,Decoration
from coupons.models import PromoCode
import time


class ADDRESS_TYPE(models.TextChoices):
    HOME_ADDRESS = "H" , "Home Address"
    OFFICE_ADDRESS = "O" , "Office Address"   
    

class COUNTRY(models.TextChoices):
    INDIA = "India", "India"
    UNITED_STATES = "US", "United States"
    UNITED_KINGDOM = "UK", "United Kingdom"
    CANADA = "CA", "Canada"
    AUSTRALIA = "AU", "Australia"
    UAE = "AE", "United Arab Emirates"
    
class OrderAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    address_type = models.CharField(max_length=1,choices=ADDRESS_TYPE.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=8,choices=COUNTRY.choices)
    landmark = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    secondary_phone_number = models.CharField(max_length=15,null=True,blank=True)
    postal_code = models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    recipient_name = models.CharField(max_length=30)
    street_address = models.CharField(max_length=200)
    apartment = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    )

    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )
    delivery_address = models.ForeignKey(
        OrderAddress,on_delete=models.CASCADE
        )
    gift_message = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    promo_code = models.ForeignKey(
        PromoCode,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    box_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES
    )
    is_cod = models.BooleanField(default=False)
    products_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    decorations_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    #
    delivery_date = models.DateTimeField(
        blank=True,
        null=True
    )

    expected_delivery = models.DateTimeField(
        blank=True,
        null=True
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    
    def order_number_generator(self):
        timestamp = int(time.time())
        id = self.id
        return f"OD{id}{timestamp}"
        

    
    
class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    product_name = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=100, blank=True, null=True)

    color_name = models.CharField(max_length=50, blank=True, null=True)
    size_name = models.CharField(max_length=50, blank=True, null=True)

    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    price_at_order_time = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    product_image = models.ImageField(
    upload_to='order_items/',
    null=True,
    blank=True
)
    

    
    
class OrderHamper(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='order_hampers'
    )

    
    hamper = models.ForeignKey(
        HamperBox,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    hamper_name = models.CharField(max_length=255)
    category_name = models.CharField(max_length=100)

    size_label = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=5, decimal_places=2)

    box_price_at_order_time = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    box_image = models.ImageField(
    upload_to='order_items/',
    null=True,
    blank=True
)



class OrderDecoration(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='order_decorations'
    )
    decoration = models.ForeignKey(
        Decoration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    decoration_name = models.CharField(max_length=255)

    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=5, decimal_places=2)

    is_inside = models.BooleanField(default=False)
    is_outside = models.BooleanField(default=False)

    price_at_order_time = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    