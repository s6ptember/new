# admin.py в приложении users
from django.contrib import admin
from .models import User, Installment, InstallmentPayment 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class InstallmentPaymentInline(admin.TabularInline):
    model = InstallmentPayment
    extra = 0  

class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'months', 'total_price', 'monthly_payment', 'created_at', 'completed')
    list_filter = ('completed',)
    search_fields = ('user__phone_number', 'product__name')  # Изменено на phone_number
    ordering = ('-created_at',)
    inlines = [InstallmentPaymentInline] 

class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_active', 'can_take_installment')  # Изменено на phone_number
    list_filter = ('is_staff', 'is_active', 'can_take_installment')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),  # Изменено на phone_number
        ('Личная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'city', 'postal_code', 'street', 'house_number', 'apartment_number')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Права на рассрочку', {'fields': ('can_take_installment',)}),  # Новое поле
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'can_take_installment')}
        ),
    )
    search_fields = ('phone_number',)  # Изменено на phone_number
    ordering = ('phone_number',)  # Изменено на phone_number

admin.site.register(User, UserAdmin)
admin.site.register(Installment, InstallmentAdmin)