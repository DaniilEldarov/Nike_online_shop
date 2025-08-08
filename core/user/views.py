from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import EmailVerificationCode
import random

User = get_user_model()


# ==================
# РЕГИСТРАЦИЯ
# ==================
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Такой email уже зарегистрирован'})

        # Создаём пользователя (но пока не активируем)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Генерация кода
        code = str(random.randint(100000, 999999))
        EmailVerificationCode.objects.create(user=user, code=code)

        # Отправка кода
        send_mail(
            'Код подтверждения регистрации',
            f'Ваш код: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        request.session['pending_user_id'] = user.id
        return redirect('verify_register')

    return render(request, 'register.html')


# ==================
# ПОДТВЕРЖДЕНИЕ РЕГИСТРАЦИИ
# ==================
def verify_register_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_id = request.session.get('pending_user_id')

        try:
            user = User.objects.get(id=user_id)
            ver_code = EmailVerificationCode.objects.filter(user=user, code=code).latest('created_at')
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'verify_register.html', {'error': 'Неверный код'})

    return render(request, 'verify_register.html')


# ==================
# ВХОД (ШАГ 1 — проверка логина/пароля и отправка кода)
# ==================
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            code = str(random.randint(100000, 999999))
            EmailVerificationCode.objects.create(user=user, code=code)

            send_mail(
                'Код подтверждения входа',
                f'Ваш код: {code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            request.session['login_user_id'] = user.id
            return redirect('verify_login')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')


# ==================
# ВХОД (ШАГ 2 — проверка кода)
# ==================
def verify_login_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_id = request.session.get('login_user_id')

        try:
            user = User.objects.get(id=user_id)
            ver_code = EmailVerificationCode.objects.filter(user=user, code=code).latest('created_at')
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'verify_login.html', {'error': 'Неверный код'})

    return render(request, 'verify_login.html')


# ==================
# ВЫХОД
# ==================
def logout_user(request):
    logout(request)
    return redirect('login')
