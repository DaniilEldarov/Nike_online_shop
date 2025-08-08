from django.db import models
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    cover = models.ImageField(upload_to='category_covers/', verbose_name="Обложка категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    size = models.CharField(max_length=50, verbose_name="Размер")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    stock_quantity = models.IntegerField(verbose_name="Количество на складе")
    cover = models.ImageField(upload_to='product_covers/', verbose_name="Обложка товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")

    def __str__(self):
        return f"Изображение для {self.product.name}"

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=50, verbose_name="Статус заказа")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    quantity = models.IntegerField(verbose_name="Количество")
    order = models.ManyToManyField(Order, verbose_name="Заказ")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f"Корзина пользователя {self.user}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    cart = models.ManyToManyField(Cart, verbose_name="Корзина")
    quantity = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'


class ProductRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()  # от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # чтобы один пользователь мог голосовать только один раз

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'