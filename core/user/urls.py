from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-register/', views.verify_register_view, name='verify_register'),

    path('login/', views.login_user, name='login'),
    path('verify-login/', views.verify_login_view, name='verify_login'),

    path('logout/', views.logout_user, name='logout'),
]
