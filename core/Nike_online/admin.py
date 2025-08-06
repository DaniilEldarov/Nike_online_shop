from django.contrib import admin
from .models import User, Product, Category, Image, Order, OrderItem, Cart, CartItems

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    # Указываем явно, что Image связана через Product.id_Image
    fk_name = 'product'  # Это не будет работать, так как у вас связь в другую сторону
    # В вашем случае Image не имеет прямой связи с Product, поэтому Inline нужно убрать

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'size', 'stock_quantity')
    list_filter = ('size',)
    search_fields = ('name', 'description')
    # Убрали ImageInline, так как связь идет от Product к Image, а не наоборот

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_Product')
    raw_id_fields = ('id_Product',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('id_Product',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_User', 'order_date', 'status', 'total_price')
    list_filter = ('status', 'order_date')
    search_fields = ('id_User__username',)
    inlines = [OrderItemInline]

class CartItemsInline(admin.TabularInline):
    model = CartItems
    extra = 1
    raw_id_fields = ('id_Product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_User')
    search_fields = ('id_User__username',)
    inlines = [CartItemsInline]

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)