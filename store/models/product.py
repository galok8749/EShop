from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=50)
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='uploads/products/')