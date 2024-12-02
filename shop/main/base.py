# views/base.py
from django.views.generic import TemplateView
from .models import Category, SubCategory

class BaseContextView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context