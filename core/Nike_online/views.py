from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Product, Category, Cart,CartItems


def detail_page(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request,'side/single-product.html',{'product':product})


@login_required(login_url='/login/')
def add_product_cart(request,product_id,quantity,):
    product = Product.objects.filter(id=product_id).first()
    cart , _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItems(product=product,cart=cart,quantity=quantity )
    cart_items.save()
    messages.success(request, 'Successfully added to cart')
