from django.db import models
from order.models import Order
from django.conf import settings



RETURN_STATUS_CHOICES = (
    ('REQUESTED', 'Requested'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('PICKED_UP', 'Picked Up'),
    ('REFUNDED', 'Refunded'),
)

class OrderReturn(models.Model):
    description = models.TextField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=RETURN_STATUS_CHOICES,default='REQUESTED')
    refund_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_refunded = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True,blank=True)
    

class ReturnImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='return_images/')
    return_request = models.ForeignKey(OrderReturn,on_delete=models.CASCADE,related_name='images')
    
   
class ReturnVideo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='return_video/')
    return_request = models.ForeignKey(OrderReturn,on_delete=models.CASCADE,related_name='videos')
    
