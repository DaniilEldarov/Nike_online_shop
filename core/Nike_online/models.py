# Create your models here.
from django.db import models

from user.models import MyUser



class Category(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='category_covers/')


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    cover = models.ImageField(upload_to='product_covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    User = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class OrderItem(models.Model):
    quantity = models.IntegerField()
    order = models.ManyToManyField(Order)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    cart = models.ManyToManyField(CartItems)


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)],blank=True,null=True)