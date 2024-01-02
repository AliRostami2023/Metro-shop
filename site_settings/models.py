from django.db import models
from django.utils.html import format_html


class Setting(models.Model):
    site_name = models.CharField(max_length=300, verbose_name='site name')
    site_url = models.URLField(null=True, blank=True, verbose_name='url')
    logo_site = models.ImageField(upload_to='uploads/logo_site', null=True, blank=True, verbose_name='logo site')
    facebook = models.URLField(null=True, blank=True)
    twitterX = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    pinterest = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    number_customer_support = models.CharField(max_length=30, verbose_name='number customer support')
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=30)
    fax = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=700)
    copy_right = models.CharField(max_length=500)
    about_us = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name

    def logo(self):
        return format_html('<img src = "{}" width=22% height=70px>'.format(self.logo_site.url))

    class Meta:
        verbose_name = 'setting'
        verbose_name_plural = 'settings site'


class FooterBox(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'box'
        verbose_name_plural = 'footer boxes'


class FooterLink(models.Model):
    box = models.ForeignKey(FooterBox, on_delete=models.SET_NULL, null=True, blank=True, related_name='boxes')
    title = models.CharField(max_length=200)
    url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'footer links'
