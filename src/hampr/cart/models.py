from django.db import models
import uuid
from decimal import Decimal


from catalog.models import HamperBox,BoxSize,ProductVariant,Decoration
from accounts.models import CustomUser
from catalog.utilts import voulme_calculater



class CustomHamper(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    box = models.ForeignKey(HamperBox,on_delete=models.CASCADE)
    box_size = models.ForeignKey(BoxSize,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='current_cart')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    
    
    def get_products_json(self):
        return [
            {
                "id": item.product_varient.id,
                "name": item.product_varient.product.name,
                "quantity": item.quantity,
                "price": item.product_varient.price,
                "total": item.quantity * item.product_varient.price,
                 "variant_label": (
                                        item.product_varient.size.name
                                        if item.product_varient.size
                                        else item.product_varient.color.name
                                        if item.product_varient.color
                                        else ""
                                    ),
            }
            for item in self.cart_products.all()
        ]
    def get_products_total(self):
        sum = 0
        for item in self.cart_products.all():
            sum += item.quantity * item.product_varient.price
        return sum
    
    def get_decoration_total(self):
        sum = 0
        for item in self.cart_decoartion.all():
            sum += item.quantity * item.decoration.price
        return sum
    def get_grand_total(self):
        sum = 0
        sum = self.box_size.price
        sum += self.get_products_total()
        sum += self.get_decoration_total()
        return sum
    def get_used_volume(self):
        total  = 0
        for i in self.cart_products.all():
            total += (voulme_calculater(i.product_varient.height,i.product_varient.width,i.product_varient.depth) * i.quantity)
        for i in self.cart_decoartion.all().filter(position='inner'):
            total +=( voulme_calculater(i.decoration.height,i.decoration.width,i.decoration.depth) * i.quantity)
        
        return total
        
        
        

class CartProduct(models.Model):
    cart = models.ForeignKey(CustomHamper,on_delete=models.CASCADE,related_name='cart_products')
    quantity = models.IntegerField(default=1)
    product_varient = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    
    def get_line_total(self):
        return self.product_varient.price * self.quantity
    
    
class CartDecoration(models.Model):
    POSITION_CHOICES = [
        ('outer','Outer Decoration'),
        ('inner','Inner Decoration')
    ]
    cart = models.ForeignKey(CustomHamper,on_delete=models.CASCADE,related_name='cart_decoartion')
    decoration = models.ForeignKey(Decoration,on_delete=models.CASCADE)
    position = models.CharField(max_length=10,choices=POSITION_CHOICES)
    quantity = models.IntegerField(default=1)
    
    
    def get_line_total(self):
        return self.decoration.price * self.quantity

    