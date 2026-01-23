from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import OrderReturn

ALLOWED_RETURN_REASONS = {
    'defective',
    'wrong_item',
    'not_as_described',
    'quality_issue',
    'other',
}


class OrderReturnForm(forms.ModelForm):

    class Meta:
        model = OrderReturn
        fields = ['description', 'reason']
        
        
    def clean_reason(self):
        reason = self.cleaned_data.get('reason')

        if not reason:
            raise forms.ValidationError("Please select a reason for return.")

        if reason not in ALLOWED_RETURN_REASONS:
            raise forms.ValidationError("Invalid return reason selected.")

        return reason
    
    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description or len(description.strip()) < 15:
            raise forms.ValidationError(
                "Description must be at least 15 characters long."
            )

        return description
    
    def clean(self):
        cleaned_data = super().clean()

        order = self.instance.order or self.initial.get('order')
        
        if not order:
            raise forms.ValidationError("Order Not Found")
        
        if not order.status == 'DELIVERED':
            raise forms.ValidationError("Only Return Delivered Products")

        if OrderReturn.objects.filter(order=order).exists():
            raise forms.ValidationError("Already Requested The Return")
        
        
        if order.delivered_at:
            if timezone.now() > order.delivered_at + timedelta(days=7):
                raise forms.ValidationError(
                    "The return period for this order has expired."
                )

        return cleaned_data
