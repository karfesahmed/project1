from django.db import models
from autoslug import AutoSlugField
from django.db import transaction



class Category(models.Model):
    name = models.CharField(max_length=64,unique=True)
    slug = AutoSlugField(populate_from='name',unique=True)
    image = models.ImageField(upload_to='categories/',blank=True,null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)
    slug = AutoSlugField(populate_from='name',unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,blank=True,null=True, on_delete=models.SET_NULL, related_name="products")
    def __str__(self):
        return self.name
    

class Size(models.Model):
    size = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    def __str__(self):
        return self.size
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["size","product"], 
                name="unique_size"
            )
        ]


class Color(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='colors/',blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    def __str__(self):
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name","product"],
                name="unique_color"
            )
        ]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    order = models.PositiveSmallIntegerField(blank=True)
    is_primary = models.BooleanField(default=False,blank=True)
    @property
    def last_order(self):
        last_image = ProductImage.objects.filter(product=self.product).order_by("order").last()
        if last_image:
            return last_image.order
        else:
            return -1
        
    def save(self,**kwargs):
        if not self.pk:
            self.order = self.last_order+1

            has_primary = ProductImage.objects.filter(
                            product = self.product,
                            is_primary = True
                            ).exists()
            if not self.is_primary:
                if not has_primary:
                    self.is_primary = True

            else:
                if has_primary:
                    ProductImage.objects.filter(
                                    product=self.product
                                    ).update(is_primary=False)
            
        elif self.is_primary:
            ProductImage.objects.filter(
                product=self.product
                ).exclude(pk=self.pk).update(is_primary=False)
        elif not self.is_primary:
            images_exists = ProductImage.objects.filter(
                            product=self.product,is_primary=True
                            ).exclude(pk=self.pk).exists()
            if not images_exists:
                imgs = ProductImage.objects.filter(
                            product=self.product
                            ).exclude(pk=self.pk)
                if imgs.exists():
                    i = imgs.first()
                    ProductImage.objects.filter(pk=i.pk).update(is_primary=True)
                else:
                    self.is_primary=True

        return super().save(**kwargs)
        
        
    def delete(self,**kwargs):    
        if self.is_primary:
            with transaction.atomic():
                img = ProductImage.objects.filter(
                                product=self.product
                                ).exclude(pk=self.pk).first()
                super().delete(**kwargs)
                if img:
                    ProductImage.objects.filter(pk=img.pk).update(is_primary=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product","order"],
                name="unique_order"
            ),
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="unique_primary"
            )
        ]


