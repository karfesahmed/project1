from django.db import models
from accounts.models import User
class StoreProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="store_profile")
    store_name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='store/logo/', blank=True, null=True)
    banner = models.ImageField(upload_to='store/banner/', blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name