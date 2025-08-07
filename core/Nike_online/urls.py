from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *
urlpatterns = [
    #Products
    path('detail_product/<int:product_id>', detail_page, name='detail'),
    path('add_product_cart/<int:product_id>/<int:quantity>', add_product_cart, name='add_product_cart'),

    #About
    path('about/',about_view, name='about'),
]