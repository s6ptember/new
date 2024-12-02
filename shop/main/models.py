from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from django.conf import settings
from gtts import gTTS
import os
import random
import string


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, 
                            blank=True, null=True, verbose_name='URL')
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]


class SubCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                               null=True, blank=True, 
                               related_name='subcategories', verbose_name='родитель')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='subcategories', null=True,
                                 blank=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, 
                            blank=True, null=True, verbose_name='URL')


    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        
        
def generate_unique_sku():
    """Генерация уникального артикула из 6 случайных символов."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


class Product(models.Model):
    sku = models.CharField(max_length=6, unique=True, 
                           default=generate_unique_sku,
                           verbose_name='Артикул')
    category = models.ForeignKey(Category, related_name='products', 
                                 on_delete=models.CASCADE,
                                 null=True, blank=True, 
                                 verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory, related_name='products', 
                                    on_delete=models.CASCADE, 
                                    null=True, blank=True, 
                                    verbose_name='Подкатегория')
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='URL')
    image = models.ImageField(upload_to='products/%Y/%m/%d', 
                              blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, 
                                   verbose_name='Скидка')
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True, 
                                  verbose_name='Аудио')


    def clean(self):
        if not self.category and not self.subcategory:
            raise ValidationError('Продукт должен принадлежать либо категории, либо подкатегории.')


    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_unique_sku()
        super().save(*args, **kwargs)
        if not self.audio_file:
            self.generate_audio()
        
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
    

    def generate_audio(self):
        text = f"Название: {self.name}. Описание: {self.description}. Цена: {self.price} рублей."
        tts = gTTS(text=text, lang='ru')
        
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        os.makedirs(audio_dir, exist_ok=True) 
        audio_file_path = os.path.join(audio_dir, f"{self.sku}.mp3")
        tts.save(audio_file_path)
        
        self.audio_file = f"audio/{self.sku}.mp3"  
        self.save(update_fields=['audio_file']) 


    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    
    
    def __str__(self):
        return f'{self.product.name} - {self.image.name}'
        

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='favorites', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='favorited_by', verbose_name='Продукт')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    