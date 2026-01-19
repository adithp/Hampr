from django.core.mail import send_mail
from django.conf import settings
import threading
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.http import HttpResponse

from xhtml2pdf import pisa
from io import BytesIO


def sendmail(address,subject,message):
    def sendmail_thread():
        send_mail(subject,message,settings.EMAIL_HOST_USER,[address])

    
    mail_thread = threading.Thread(target=sendmail_thread)
    mail_thread.start()
FMT = "%d-%m-%Y %H:%M:%S"

def invoice_generator(order):
    invoice_html = render_to_string('c_admin/invoice.html',context={'order':order})
    result = BytesIO()
    pdf = pisa.CreatePDF(invoice_html, dest=result)
    if pdf.err:
        return HttpResponse("PDF generation error", status=500)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{order.order_number}.pdf"'
    )
    return response
            
        
        
        
    