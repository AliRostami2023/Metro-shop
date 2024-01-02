from django.contrib import admin
from . import models


# Register your models here.

class FooterLinkInline(admin.TabularInline):
    model = models.FooterLink


@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_url', 'logo', 'email', 'active']


@admin.register(models.FooterBox)
class FooterBoxAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [FooterLinkInline]

