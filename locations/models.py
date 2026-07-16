from django.db import models

# Create your models here.
class Wilaya(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)
    ar_name = models.CharField(max_length=64)
    delivery_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya,on_delete=models.CASCADE,related_name="communes")
    name = models.CharField(max_length=64)
    ar_name = models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return self.name
