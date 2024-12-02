from django.shortcuts import render
from .models import ContactInfo

def delivery_view(request):
    contact_info = ContactInfo.objects.first() 
    return render(request, 'info/delivery.html', 
                  {'contact_info': contact_info})
    
def contact_view(request):
    contact_info = ContactInfo.objects.first() 
    return render(request, 'info/contacts.html', 
                  {'contact_info': contact_info})