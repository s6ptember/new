# orders/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart
from decimal import Decimal


# orders/views.py
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            total_price = sum(
                (Decimal(item['price']) - (Decimal(item['price']) * (Decimal(item['product'].discount) / 100))) * item['quantity']
                for item in cart if 'product' in item)
            
            order.total_price = total_price
            order.save()

            for item in cart:
                product = item.get('product')
                if product:  
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price'] * (1 - product.discount / 100)  
                    )

            cart.clear()  
            return redirect('orders:order_success', order_id=order.id)
    else:
        form = OrderForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'middle_name': request.user.middle_name,
            'phone_number': request.user.phone_number,
            'city': request.user.city,
            'postal_code': request.user.postal_code,
            'street': request.user.street,
            'house_number': request.user.house_number,
            'apartment_number': request.user.apartment_number,
        })
    return render(request, 'orders/order_form.html', {'form': form, 'cart': cart})


@login_required
def order_success(request, order_id):
    # Получаем последний заказ пользователя по его ID
    order = Order.objects.filter(id=order_id, user=request.user).first()
    if order is None:
        return redirect('orders:order_create')  # Если заказ не найден, перенаправляем на создание заказа
    return render(request, 'orders/order_success.html', {'order': order})