from django.core.mail import send_mail
from django.conf import settings
import threading
from django.contrib.auth.decorators import user_passes_test


def sendmail(address,subject,message):
    def sendmail_thread():
        send_mail(subject,message,settings.EMAIL_HOST_USER,[address])

    
    mail_thread = threading.Thread(target=sendmail_thread)
    mail_thread.start()
FMT = "%d-%m-%Y %H:%M:%S"
        
        
        
        
    