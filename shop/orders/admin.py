from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество пустых форм для добавления новых элементов заказа


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'total_price', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'user__email')  # Поля для поиска
    list_filter = ('created_at',)  # Фильтры для боковой панели
    inlines = [OrderItemInline]  # Встраиваем элементы заказа в интерфейс заказа

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)