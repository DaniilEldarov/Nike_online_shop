from django.contrib import admin
# Register your models here.
from .models import CartItem,Cart,Category,Product,OrderItem,Order,ProductRating,Image

admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(ProductRating)
admin.site.register(Cart)
admin.site.register(Order)



class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 1  # number of empty image slots

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]