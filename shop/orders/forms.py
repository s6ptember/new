# orders/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    # Добавляем поле для оплаты наличными
    cash_payment = forms.BooleanField(required=False, label='Оплата наличными')

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'middle_name',
            'phone_number', 'city', 'postal_code',
            'street', 'house_number', 'apartment_number',
            'cash_payment'  # Добавляем поле для оплаты наличными в список полей
        )