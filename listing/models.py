from django.db import models

class Share(models.Model):
    name = models.CharField(max_length=254, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    previous_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

class Commodity(models.Model):
    name = models.CharField(max_length=254, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    previous_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name
