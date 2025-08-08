from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.contrib import admin
from .views import *
urlpatterns = [
    path('detail_product/<int:product_id>', detail_page, name='detail'),
    path('add_product_cart/<int:product_id>/<int:quantity>', add_product_cart, name='add_product_cart'),
    path('', include('user.urls')),
]