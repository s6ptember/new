from django.db import models
from main.models import Product
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=30, blank=True, 
                                   verbose_name='Отчество')
    phone_number = models.CharField(max_length=15, blank=True, 
                                    verbose_name='Номер телефона')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    postal_code = models.CharField(max_length=10, blank=True, 
                                   verbose_name='Почтовый индекс')
    street = models.CharField(max_length=100, blank=True, 
                              verbose_name='Улица')
    house_number = models.CharField(max_length=10, blank=True, 
                                    verbose_name='Номер дома')
    apartment_number = models.CharField(max_length=10, blank=True, 
                                        verbose_name='Номер квартиры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, 
                                      verbose_name='Итоговая цена')
    cash_payment = models.BooleanField(default=False, verbose_name='Оплата наличными')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id} by {self.user.phone_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, 
                              verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, 
                                verbose_name='Цена')
    

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    