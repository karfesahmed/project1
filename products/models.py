from itertools import product

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='categories/')
    def __str__(self):
        return self.name

class Price(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)
    price = models.OneToOneField(Price,on_delete=models.CASCADE, related_name="product") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,blank=True,null=True, on_delete=models.SET_NULL, related_name="products")
    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=250)
    price = models.OneToOneField(Price, on_delete=models.CASCADE, related_name='size')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    def __str__(self):
        return self.size

class Color(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='colors/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')