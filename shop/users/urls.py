from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registration/', views.register, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites-list/', views.favorites_list, name='favorites_list'),
    path('add_to_favorites/<str:sku>/', 
         views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:sku>/', 
         views.remove_from_favorites, name='remove_from_favorites'),
    # path('logout/', views.logout, name='logout'),
]
    

