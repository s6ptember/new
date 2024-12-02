# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number', 'password1', 'password2')  # Используем номер телефона


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label=("Номер телефона"))  # Поле для номера телефона
    password = forms.CharField(widget=forms.PasswordInput, label=("Пароль"))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name',
                  'phone_number', 'city', 'postal_code', 
                  'street', 'house_number', 'apartment_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Введите отчество'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}),
            'city': forms.TextInput(attrs={'placeholder': 'Введите город'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Введите почтовый индекс'}),
            'street': forms.TextInput(attrs={'placeholder': 'Введите улицу'}),
            'house_number': forms.TextInput(attrs={'placeholder': 'Введите номер дома'}),
            'apartment_number': forms.TextInput(attrs={'placeholder': 'Введите номер квартиры'}),
        }