from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import MyUser  # or MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email','username')


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email','is_2fa_enabled']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_2fa_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }