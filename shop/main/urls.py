from django.urls import path
from .views import ProductListView, ProductDetailView


app_name = 'index'

urlpatterns = [
    path('',
         ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', 
         ProductListView.as_view(), name='product_list_by_category'),
    path('products/category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/', 
         ProductListView.as_view(), name='product_list_by_subcategory'),
    path('product/<str:sku>/', ProductDetailView.as_view(), name='product_detail'),
]