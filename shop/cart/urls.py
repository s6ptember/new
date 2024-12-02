from django.urls import path
from .views import cart_add, cart_remove, cart_detail, take_installment

app_name = 'cart'

urlpatterns = [
    path('add/<str:sku>/', cart_add, name='cart_add'),  # Изменено на sku
    path('remove/<str:sku>/', cart_remove, name='cart_remove'),
    path('take_installment/<str:sku>/', take_installment, name='take_installment'),# Изменено на sku
    path('', cart_detail, name='cart_detail'),
]