from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('verify_code/<int:user_id>', verify_code, name='verify_code'),
    path('resend_code/<int:user_id>',resend_code,name='resend_code'),
    path('profile_view/',profile_view,name='profile'),
]