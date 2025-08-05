from django.contrib import admin
# Register your models here.
from .models import CartItems,Cart,Category,Product,OrderItem,Order,Rating

admin.site.register(CartItems)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Order)