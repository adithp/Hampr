import random,uuid,hashlib
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta,datetime

from .models import OTP,PasswordReset
from core.utils import sendmail,FMT







def otp_gen():
    return random.randint(1000,9999)


def otp_create(user,otp_code,otp_delivery,otp_type):
    otp_obj = OTP(user=user,otp_code=otp_code,otp_type=otp_type,otp_delivery=otp_delivery, expires_at = timezone.now() + timedelta(minutes=5))
    obj = otp_obj.save()
    return otp_obj


def otp_send_signup(request,user):
        otp_code = otp_gen()

                
        obj = otp_create(user=user,otp_code=otp_code,otp_delivery='E',otp_type='EV')
        message = f'Your hampr signup otp is {otp_code}'
        sendmail(address=user.email,subject='Signup Otp for Hampr',message=message)
        request.session['otp_pending'] = True
        request.session['otp_pending_user_id'] = user.id
        count = request.session.get('otp_send_count',0)
        if count:
            request.session['otp_send_count'] = count + 1
        else:
            request.session['otp_send_count'] = 1
            
        
            
        

def otp_block_time_verify(req):
    now = timezone.now()
    block_time = req.session.get('block_time',{})
    if block_time:
        block_time = datetime.strptime(block_time,FMT)
        block_time = timezone.make_aware(block_time)
        if block_time > now:
            total_seconds = int((block_time-now).total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"You need to wait {hours} hours and {minutes} minutes to wait to resend otp"
        return True
    return True
    
    

def password_reset_link(user):
    raw_token = str(uuid.uuid4())
    token = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    obj = PasswordReset(user=user,token=token)
    obj.save()
    message = f"""
    We received a request to reset the password for your Hampr account.

If you made this request, you can set a new password using the link below:

Reset Password: http://127.0.0.1:8000/auth/reset_password/{raw_token}/ 

This link will remain valid for 1 hour.

If you did not request a password reset, please ignore this email — your account is safe.

Thank you,
Hampr Support Team
"""
    sendmail(user.email,'Hampr — Password Reset Request',message)
    
    
    
def token_checker(raw_token):
    token = hashlib.sha256(str(raw_token).encode('utf-8')).hexdigest()
    try:
        token_obj = PasswordReset.objects.get(token=token)
    except:
        return False
    if token_obj.is_expired():
        return False
    return token_obj