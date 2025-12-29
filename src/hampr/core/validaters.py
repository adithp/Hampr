import re
from django.core.exceptions import ValidationError


def validate_indian_phone_number(value):
    pattern = r'\+91[6-9]\d{9}'
    if not re.match(pattern,value):
        raise ValidationError("Make sure the number MUST start and end exactly like +91xxxxxxxxxx")
    

def no_all_digits(value):
    if value.isdigit():
        raise ValidationError('Username cannot be all numbers')
    
    
def username_validater(value):
    pattern = r'[a-zA-z1-9_]'
    if not re.match(pattern,value):
        raise ValidationError('username only contain alphabets and numbers and _')



def validate_image(image):
    valid_types = ['image/jpeg', 'image/png', 'image/webp']

    if image.file.content_type not in valid_types:
        raise ValidationError("Only JPG, PNG and WEBP images are allowed")