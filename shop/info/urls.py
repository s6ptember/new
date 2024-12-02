from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('delivery/', views.delivery_view, name='delivery'),
    path('contacts/', views.contact_view, name='contacts'),
]