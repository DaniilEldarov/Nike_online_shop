from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    address = models.TextField()

    def __str__(self):
        return self.username


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image {self.id}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.TextField()
    stock_quantity = models.IntegerField()
    cover = models.ImageField(upload_to='product_covers/')
    id_Image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='category_covers/')
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    id_User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    quantity = models.IntegerField()
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Item {self.id} in Order {self.id_order_id}"


class Cart(models.Model):
    id_User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.id} for {self.id_User.username}"


class CartItems(models.Model):
    id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_basket = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.id_Product.name} in cart {self.id_basket.id}"
