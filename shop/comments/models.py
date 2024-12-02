from django.db import models
from django.conf import settings
from main.models import Product
from orders.models import Order


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             related_name='reviews', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                 related_name='reviews', verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name='reviews', verbose_name='Заказ')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', choices=[
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ])
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        unique_together = ('user', 'product')  # Один отзыв от пользователя на продукт


    def __str__(self):
        return f'Отзыв {self.rating} от {self.user.phone_number} на {self.product.name}'