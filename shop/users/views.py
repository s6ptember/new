# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProfileForm
from django.contrib.auth import logout
from main.models import Product, Favorite
from orders.models import Order
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя
            user = form.save()  # Предполагается, что форма имеет метод save()
            # Выполняем вход для нового пользователя (опционально)
            login(request, user)
            return redirect('users:profile')  # Перенаправляем на профиль или другую страницу
    else:
        form = RegistrationForm()   
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                form.add_error(None, 'Неверный номер телефона или пароль.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', {'form': form, 'orders': orders})

@login_required
def logout_view(request):
    logout(request)  # Выход из аккаунта
    return redirect('index:product_list')

@login_required
def add_to_favorites(request, sku):
    product = get_object_or_404(Product, sku=sku)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index:product_list'))

@login_required
def remove_from_favorites(request, sku):
    product = get_object_or_404(Product, sku=sku)  
    Favorite.objects.filter(user=request.user, product=product).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index:product_list'))

def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'users/favorites_list.html', {'favorites': favorites})