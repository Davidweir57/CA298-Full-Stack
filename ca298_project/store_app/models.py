from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class ProductSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.FileField(upload_to='product_img/', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)


class ProductStock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()


class CaUser(AbstractUser):
    is_admin = models.BooleanField(default=False)


class ShoppingBasket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CaUser, on_delete=models.CASCADE)


class ShoppingBasketItems(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CaUser, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    shipping_addr = models.CharField(max_length=500)
    card_num = models.CharField(max_length=16)


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def price(self):
        return self.product.price * self.quantity






