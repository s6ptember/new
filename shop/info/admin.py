from django.contrib import admin
from .models import ContactInfo
from .models import Banner


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'courier_delivery', 'delivery_in_russia', 
                    'cash_payment', 'cash_on_delivery', 'electronic_money',
                    'address', 'manager_phone', 'timetable', 'mail')
    search_fields = ('phone_number',)



class BannerAdmin(admin.ModelAdmin):
    list_display = ('url', 'image')
    search_fields = ('url',)

admin.site.register(Banner, BannerAdmin)