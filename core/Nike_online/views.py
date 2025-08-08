from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Category, Cart,CartItem, ProductRating

def index(request):
    products = Product.objects.all()
    return render(request, 'main/index.html', {'products': products})

def detail_page(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request,'side/single-product.html',{'product':product})

def category_view(request):
    categories = Category.objects.all()
    category_products = {}

    for category in categories:
        products = Product.objects.filter(category=category)

        for product in products:
            ratings = product.ratings.all()
            product.avg_rating = round(sum(r.rating for r in ratings) / len(ratings), 1) if ratings else 0
            product.user_rating = None
            if request.user.is_authenticated:
                user_rating = ratings.filter(user=request.user).first()
                if user_rating:
                    product.user_rating = user_rating.rating

        category_products[category.name] = products

    return render(request, 'main/category.html', {'category_products': category_products})

@login_required(login_url='/login/')
def add_product_cart(request,product_id,quantity,):
    product = Product.objects.filter(id=product_id).first()
    cart , _ = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem(product=product,cart=cart,quantity=quantity )
    cart_item.save()
    messages.success(request, 'Successfully added to cart')

@csrf_exempt
@login_required
def rate_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    product_id = data.get('product_id')
    rating = data.get('rating')

    product = Product.objects.get(id=product_id)
    user = request.user

    product_rating, created = ProductRating.objects.update_or_create(
        user=user,
        product=product,
        defaults={'rating': rating}
    )
    return JsonResponse({'success': True, 'rating': rating})
