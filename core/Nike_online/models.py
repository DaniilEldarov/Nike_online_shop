# Create your models here.
from django.db import models

from user.models import MyUser


class Image(models.Model):
    image = models.ImageField(upload_to='medis/product_images/')


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.TextField()
    stock_quantity = models.IntegerField()
    cover = models.ImageField(upload_to='product_covers/')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='category_covers/')
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    id_User = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class OrderItem(models.Model):
    quantity = models.IntegerField()
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    id_User = models.ForeignKey(MyUser, on_delete=models.CASCADE)



class CartItems(models.Model):
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_basket = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

