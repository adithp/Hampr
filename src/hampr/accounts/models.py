from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils import timezone
from datetime import timedelta
import uuid
from django.core.validators import MinLengthValidator,MaxLengthValidator


from core.validaters import validate_indian_phone_number,no_all_digits,username_validater


class Gender(models.TextChoices):
    MALE = "M" , "Male"
    FEMALE = "F" , "Female"
    OTHER = "O" , "Other"
    
    
class OTP_DELIVERY(models.TextChoices):
    EMAIL = "E", "Email"
    PHONE = "P", "Phone"
    

class OTP_TYPE(models.TextChoices):
    EMAIL_VERIFICATION = "EV" , "Email Verification"
    LOGIN = "2F" , "Two Factor Authentication"
    PASSWORD_RESET = "PR" , "Password Reset"
    PHONE_UPDTAE = "PU" , "Phone Update"
    

class ADDRESS_TYPE(models.TextChoices):
    HOME_ADDRESS = "H" , "Home Address"
    OFFICE_ADDRESS = "O" , "Office Address"   
    

class COUNTRY(models.TextChoices):
    INDIA = "IN", "India"
    UNITED_STATES = "US", "United States"
    UNITED_KINGDOM = "UK", "United Kingdom"
    CANADA = "CA", "Canada"
    AUSTRALIA = "AU", "Australia"
    UAE = "AE", "United Arab Emirates"
    
    
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=20,unique=True,validators=[no_all_digits,username_validater])
    dob = models.DateField(blank=True,null=True)
    email_notification = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1,choices=Gender.choices,blank=True,null=True)
    phone_number = models.CharField(max_length=13,null=True,blank=True,unique=True,validators=[validate_indian_phone_number])
    phone_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/',null=True,blank=True)
    # promotional_emails = models.BooleanField(default=True)
    # sms_notification = models.BooleanField(default=False)
    # two_factor_enabled = models.BooleanField(default=False)
    # google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    # newsletter_subscribed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_joined']

    
    
    def __str__(self):
        return self.username
    
    
class OTP(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6)
    otp_type = models.CharField(choices=OTP_TYPE.choices,max_length=2)
    otp_delivery = models.CharField(choices=OTP_DELIVERY.choices,max_length=1)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    

    
class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    token = models.CharField(max_length=64,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def is_expired(self):
        time = timezone.now() - self.created_at
        return time > timedelta(minutes=60)   
    
    

class UserAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    address_type = models.CharField(max_length=1,choices=ADDRESS_TYPE.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=3,choices=COUNTRY.choices)
    landmark = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    secondary_phone_number = models.CharField(max_length=15,null=True,blank=True)
    postal_code = models.IntegerField(validators=[MinLengthValidator(100000),MaxLengthValidator(999999)])
    recipient_name = models.CharField(max_length=30)
    street_address = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    
# class UserDevice(models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     device_name = models.CharField(max_length=100)
#     device_type = models.CharField(max_length=100)
#     first_accessed = models.DateTimeField(auto_now_add=True)
#     ip_address = models.GenericIPAddressField(protocol='both')
#     is_active = models.BooleanField(default=True)
#     last_accessed = models.DateTimeField(auto_now=True)
#     location = models.CharField(max_length=255,null=True,blank=True)
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    

# class UserWishlist(models.Model):
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)
#     hamper_template = models.ForeignKey()
    
    
class AuditLog(models.Model):
    entity_id = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(protocol='both',null=True,blank=True)
    old_value = models.TextField(null=True,blank=True)
    new_value = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    
    
    
    
    
    

