from django.shortcuts import render, redirect, \
    get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from users.models import Installment, InstallmentPayment
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta


@require_POST
def cart_add(request, sku):
    cart = Cart(request)
    product = get_object_or_404(Product, sku=sku)  # Получаем продукт по SKU
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                  quantity=cd['quantity'],
                  override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, sku):
    cart = Cart(request)
    product = get_object_or_404(Product, sku=sku)  # Получаем продукт по SKU
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
def take_installment(request, sku):
    if request.method == 'POST':
        months = int(request.POST.get('months'))
        if 3 <= months <= 9:
            product = get_object_or_404(Product, sku=sku)
            total_price = product.price  # Предполагается, что у вас есть поле price в модели Product
            installment = Installment.objects.create(
                user=request.user,
                product=product,
                months=months,
                total_price=total_price  # Сохраняем полную цену товара
            )
            # Создание платежей
            installment.create_payments()  # Создаем платежи
            # Очистка корзины
            cart = Cart(request)
            cart.clear()
            return redirect('cart:cart_detail')
        else:
            # Обработка ошибки
            return redirect('cart:cart_detail')
