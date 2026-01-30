from django.db import models


class Ticket(models.Model):

    ISSUE_CHOICES = [
        ('order', 'Order Issue'),
        ('payment', 'Payment Issue'),
        ('delivery', 'Delivery Issue'),
        ('general', 'General Query'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    issue_type = models.CharField(
        max_length=20,
        choices=ISSUE_CHOICES
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"
