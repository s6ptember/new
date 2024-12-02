from .models import Category


def categories_and_subcategories(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return {
        'categories': categories,
    }