from django.urls import path
from .views import add_review

app_name = 'comments'

urlpatterns = [
    path('add_review/<str:sku>/', add_review, name='add_review'),
]