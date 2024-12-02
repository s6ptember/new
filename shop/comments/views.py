# comments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from main.models import Product
from orders.models import Order

@login_required
def add_review(request, sku):
    product = get_object_or_404(Product, sku=sku)
    order = Order.objects.filter(user=request.user, items__product=product).first()
    
    if not order:
        return render(request, 'comments/error.html', {'message': 'Вы должны сделать заказ на этот продукт, чтобы оставить отзыв.'})

    # Проверяем, существует ли уже отзыв от пользователя на этот продукт
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if existing_review:
                # Если отзыв уже существует, обновляем его
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
            else:
                # Если отзыва нет, создаем новый
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.order = order
                review.save()
            return redirect('index:product_detail', sku=product.sku)
    else:
        form = ReviewForm(instance=existing_review)  # Предоставляем существующий отзыв для редактирования, если он есть

    return render(request, 'comments/add_review.html', {'form': form, 'product': product})