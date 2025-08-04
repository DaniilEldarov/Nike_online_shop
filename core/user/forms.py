from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import MyUser  # or MyUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email','username')


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'avatar', 'balance','is_2fa_enabled']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_2fa_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].disabled = True