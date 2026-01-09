from django.db import models
from django.conf import settings
import uuid

from order.models import Order

class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    card_brand = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    card_last_four = models.CharField(
        max_length=4,
        null=True,
        blank=True
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    gateway_response_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    
class PaymentGatewayLog(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    payment = models.ForeignKey(
        "Payment",
        on_delete=models.CASCADE,
        related_name="gateway_logs"
    )

    gateway_name = models.CharField(
        max_length=50
    )

    request_data = models.JSONField()

    response_data = models.JSONField()

    status_code = models.CharField(
        max_length=20
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )