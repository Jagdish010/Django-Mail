from django.contrib import admin

from .models import CustomerEnquiry, CustomerFeedBack
# Register your models here.


admin.site.register(CustomerEnquiry)
admin.site.register(CustomerFeedBack)