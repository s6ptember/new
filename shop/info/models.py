from django.db import models


class ContactInfo(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    courier_delivery = models.TextField(verbose_name='Курьером по Соль-Илецку', blank=True)
    delivery_in_russia = models.TextField(verbose_name='Доставка по России', blank=True)
    cash_payment = models.TextField(verbose_name='Наличными', blank=True)
    cash_on_delivery = models.TextField(verbose_name='Наложенным платежом', blank=True)
    electronic_money = models.TextField(verbose_name='Электронными деньгами', blank=True)
    address = models.TextField(verbose_name='Наш адрес', blank=True)
    manager_phone = models.TextField(max_length=15, verbose_name='Телефон отдела продаж ', 
                                     blank=True)
    timetable = models.TextField(verbose_name='График работы отдела продаж', 
                                    blank=True)
    mail =  models.TextField(verbose_name='Электронный ящик', blank=True)


    def __str__(self):
        return self.phone_number


    class Meta:
        verbose_name = 'Контактную информацию'
        verbose_name_plural = 'Контактная информация'
        

class Banner(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', 
                              blank=True, 
                              verbose_name='Изображение')
    url = models.URLField(max_length=200, verbose_name='URL', 
                          blank=True)
    
    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'