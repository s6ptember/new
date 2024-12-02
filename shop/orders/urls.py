# orders/urls.py
from django.urls import path
from .views import order_create, order_success

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='order_create'),  # URL для создания заказа
    path('success/<int:order_id>/', order_success, name='order_success'),  # URL для страницы успешного оформления заказа
]