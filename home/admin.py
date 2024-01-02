from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'mobile', 'email', 'subject']
    search_fields = ['full_name']
