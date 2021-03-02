from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.FileField(upload_to='product_img/', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    shipping_address = models.CharField(max_length=200)
    order_date = models.CharField(max_length=20)
    email = models.CharField(max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()


class CaUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

