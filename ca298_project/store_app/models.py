from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)


