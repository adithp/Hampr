import re
from django.core.exceptions import ValidationError

def validate_indian_phone_number(value):
    pattern = r'\+91[6-9]\d{9}'
    if not re.match(pattern,value):
        raise ValidationError("Make sure the number MUST start and end exactly like +91xxxxxxxxxx")