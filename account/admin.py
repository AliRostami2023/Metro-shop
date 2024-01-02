from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'email', 'avatar','is_superuser', 'is_active']
    list_filter = ['is_superuser', 'is_active']
    search_fields = ['first_name', 'username']
    ordering = ['-id']


