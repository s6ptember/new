from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Product, Category, SubCategory
from info.models import Banner
from django.views.generic import DetailView
from cart.forms import CartAddProductForm 
from .models import Favorite
from comments.models import Review
from comments.forms import ReviewForm
from django.db.models import Q, Count, Exists, OuterRef


class ProductListView(ListView):
    model = Product
    template_name = 'main/index/index.html'
    context_object_name = 'products'
    paginate_by = 40  # Указываем количество товаров на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get('subcategory_slug')

        # Фильтрация по категории
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        # Фильтрация по подкатегории
        if subcategory_slug:
            subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
            queryset = queryset.filter(subcategory=subcategory)

        # Поиск
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Сортировка
        if self.request.GET.get('sort_by_discount'):
            queryset = queryset.filter(discount__gt=0).order_by('-discount')
        elif self.request.GET.get('sort_by_date'):
            queryset = queryset.order_by('-created')
        else:
            sort_by = self.request.GET.get('sort', '')
            if sort_by == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price')

        # Добавляем количество отзывов
        queryset = queryset.annotate(review_count=Count('reviews'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['sort_options'] = [
            {'value': 'price_asc', 'label': 'Цена по возрастанию'},
            {'value': 'price_desc', 'label': 'Цена по убыванию'},
            {'value': 'discount', 'label': 'Товары со скидкой'},
            {'value': 'date_asc', 'label': 'Сначала старые'},
            {'value': 'date_desc', 'label': 'Сначала новые'},
        ]
        context['search_query'] = self.request.GET.get('q', '')

        # Добавляем список избранных товаров в контекст
        if self.request.user.is_authenticated:
            context['favorite_products'] = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        else:
            context['favorite_products'] = []
            
        context['banners'] = Banner.objects.all()

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product/detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        sku = self.kwargs.get('sku')
        return get_object_or_404(Product, sku=sku)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        
        product = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            is_favorited = Favorite.objects.filter(user=user, product=product).exists()
        else:
            is_favorited = False

        # Добавляем отзывы в контекст
        context['is_favorited'] = is_favorited
        context['reviews'] = product.reviews.all()  # Получаем все отзывы для данного продукта
        context['review_form'] = ReviewForm()  # Добавляем форму для отзыва

        return context