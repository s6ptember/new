# comments/admin.py
from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'product')
    search_fields = ('product__name', 'comment')
    ordering = ('-created_at',)


admin.site.register(Review, ReviewAdmin)