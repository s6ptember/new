# models.py в приложении users
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Импортируем для удобного добавления месяцев


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        user = self.create_user(phone_number, password, **extra_fields)
        return user

class User(AbstractBaseUser , PermissionsMixin):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Почтовый индекс')
    street = models.CharField(max_length=100, blank=True, verbose_name='Улица')
    house_number = models.CharField(max_length=10, blank=True, verbose_name='Номер дома')
    apartment_number = models.CharField(max_length=10, blank=True, verbose_name='Номер квартиры')
    can_take_installment = models.BooleanField(default=False, verbose_name='Может брать в рассрочку')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'  # Используем номер телефона для аутентификации
    REQUIRED_FIELDS = []  # Не требуется никаких дополнительных полей

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone_number


class Installment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)  # Используйте строковую ссылку
    months = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=99999)  # Полная цена товара
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=99999)  # Сумма ежемесячного платежа


    def __str__(self):
        return f"{self.user.phone_number} - {self.product.name} - {self.months} months"


    def save(self, *args, **kwargs):
        # Рассчитываем ежемесячный платеж при сохранении
        if self.months > 0:
            self.monthly_payment = self.total_price / self.months
        super().save(*args, **kwargs)


    def create_payments(self):
        for month in range(self.months):
            due_date = self.created_at + relativedelta(months=month)
            InstallmentPayment.objects.create(installment=self, due_date=due_date)


class InstallmentPayment(models.Model):
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='payments')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)


    def __str__(self):

        return f"Payment for {self.installment.product.name} due on {self.due_date}"