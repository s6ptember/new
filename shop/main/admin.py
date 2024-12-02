from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name', 'category', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'available', 'created', 'updated')
    list_filter = ('available', 'category', 'subcategory')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku')
    inlines = [ProductImageInline]