from django.db import models

from products.models import *
from django.core.validators import MinValueValidator
from locations.models import Commune, Wilaya
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ("pending","PENDING"),
        ("confirmed","CONFIRMED"),
        ("unreachable","UNREACHABLE"),
        ("postponed","POSTPONED"),
        ("cancelled","CANCELLED"),
    ]
    DELIVERY_STATUS = [
        ("notregistered","NOTREGISTERED"),
        ("registered","REGISTERED"),
        ("dispatched","DISPATCHED"),
        ("in_transit","IN_TRANSIT"),
        ("delivered","DELIVERED"),
        ("returned","RETURNED"),
    ]
    order_status = models.CharField(max_length=64,choices=ORDER_STATUS,blank=True,default="pending")
    delivery_status = models.CharField(max_length=64,choices=DELIVERY_STATUS,blank=True,default="notregistered")
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        related_name="orders"
    )
    size = models.ForeignKey(
        Size,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="orders"
    )
    color = models.ForeignKey(
            Color,
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
            related_name="orders"
        )
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wilaya = models.ForeignKey(
        Wilaya,
        null=True, # اجباري ادخاله لكن احتمالية حذفه موجودة لذا سيصب فارغ في قاعدة البيانات و ستخزن اسم و كود الولاية في الاوردر عند اول انشاء
        on_delete=models.SET_NULL,
        related_name="orders"
    )
    wilaya_code = models.CharField(max_length=2,blank=True,null=True)
    wilaya_name = models.CharField(max_length=64,blank=True,null=True)
    commune = models.ForeignKey(
        Commune,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders"
    )
    
    product_str = models.CharField(max_length=250,blank=True,null=True)
    product_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    size_str = models.CharField(max_length=250,blank=True,null=True)
    size_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    color_str = models.CharField(max_length=64,blank=True,null=True)
    color_image = models.ImageField(upload_to='product_images/',blank=True,null=True)
    delivery_cost = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True) 
    total_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            if self.quantity <= 0:
                raise ValidationError({
                    "quantity":"Ensure this value is greater than or equal to 1."
                })
            if self.wilaya is None:
                raise ValidationError({
                    "wilaya":"A wilaya is required to create an order."
                })
            else : 
                communes = self.wilaya.communes
                if self.commune is not None:
                    if not communes.filter(pk=self.commune.pk).exists():
                        raise ValidationError({
                            "commune":f"A commune is not in {self.wilaya.name} communes"
                        })
            self.wilaya_code = self.wilaya.code
            self.wilaya_name = self.wilaya.name
            current_product = self.product
            if current_product:

                self.product_str = current_product.name
                if current_product.discount_price:
                    self.product_price = current_product.discount_price
                else:
                    self.product_price = current_product.price
            
                if not current_product.is_available : 
                    raise ValidationError({
                        "product":"Product is not is_available"
                    })
            else:
                raise ValidationError({
                    "product":"product is required"
                })
            if self.size:
                current_price = self.size
                
                if self.size.product == self.product:
                    self.size_str = current_price.size
                    if current_price.discount_price:
                        self.size_price = current_price.discount_price
                    else:
                        self.size_price = current_price.price
                else:
                    raise ValidationError({
                        "size": "This size does not belong to the selected product."
                    })

            if self.color:
                current_color = self.color
                if self.color.product == self.product:
                    self.color_str = current_color.name
                    self.color_image = current_color.image
                else:
                    raise ValidationError({
                        "color": "This color does not belong to the selected product."
                    })

            
            
            self.delivery_cost = self.wilaya.delivery_price
            if self.size_price:
                self.total_price = self.delivery_cost + self.quantity * self.size_price
            else:
                self.total_price = self.delivery_cost + self.quantity * self.product_price

        return super().save(*args, **kwargs)

class StatusHistory(models.Model):
    changed_at = models.DateTimeField(auto_now_add=True)
    new_status = models.CharField(max_length=64)
    previous_status = models.CharField(max_length=64)
    order = models.ForeignKey(
        Order,
        null=True,
        on_delete=models.SET_NULL,
        related_name="status_history"
    )

@receiver(pre_save,sender=Order)
def pre_add_change(sender,instance,**kwargs):
    if instance.pk:
        old = Order.objects.only("order_status").get(pk=instance.pk)
        instance._old_order_status = old.order_status

@receiver(post_save,sender=Order)
def post_add_change(sender,instance,created,**kwargs):
    if not created and hasattr(instance,"_old_order_status"):
        if instance._old_order_status != instance.order_status:
            StatusHistory.objects.create(
                new_status=instance.order_status,
                previous_status= instance._old_order_status,
                order = instance
                )