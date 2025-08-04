from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,MyUserUpdateForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .services import generate_otp,is_code_valid

def login_user(request):
    if request.method == 'POST':
        user = authenticate(email=request.POST['email'],password=request.POST['password'])
        if user:
            if user.is_2fa_enabled:
                code=generate_otp()
                OTP.objects.create(user=user,
                code=code)
                send_mail(
                    "This is your temporary code from BookkingHolding",
                    f"There your code don't show this code: {code} ",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('verify_code',user_id=user.id)
            else:
                login(request, user)
                messages.success('You have been logged in')
                return redirect('main_page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'user/login.html',{'form':AuthenticationForm()})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('main_page')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully and logged in')
            return redirect('main_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def verify_code(request,user_id):
    user = get_object_or_404(MyUser,id=user_id)
    if request.method == 'POST':
        user_input_code=request.POST['code']
        otp=OTP.objects.filter(code=user_input_code,user=user).last()
        if otp:
            if is_code_valid(otp):
                messages.success(request, 'Your code has been verified \n You successfully logged in')
                login(request, user)
            else:
                # ⏰ Code expired
                messages.error(request, 'Time-code expired try again later')
            return redirect('main_page')
        else:
            messages.error(request, 'Invalid code')

    return render(request, 'user/verify_otp.html', {'user': user})


def resend_code(request,user_id):
    user = MyUser.objects.get(id=user_id)
    code=generate_otp()
    otp=OTP(user=user,code=code)
    otp.save()
    code = generate_otp()
    OTP.objects.create(user=user,
                       code=code)
    send_mail(
        "This is your temporary code from BookkingHolding",
        f"There your code don't show this code: {code} ",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    return redirect('verify_code', user_id=user.id)


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Or wherever you want to go
    else:
        form = MyUserUpdateForm(instance=user)

    return render(request, 'user/profile.html', {'form': form})