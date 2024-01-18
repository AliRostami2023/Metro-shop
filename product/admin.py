from django.contrib import admin
from . import models


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = models.ImagesProduct


class ProductCommentInline(admin.TabularInline):
    model = models.CommentProduct


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'price', 'discount', 'total_price', 'availability', 'published']
    list_filter = ['discount', 'published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'category', 'brand']
    inlines = [ProductCommentInline, ProductImageInline]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'published']
    prepopulated_fields = {'url_title': ('title',)}


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'published']
    prepopulated_fields = {'url_title': ('title',)}


@admin.register(models.ImagesProduct)
class ImagesProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_other']


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_slide', 'published']


@admin.register(models.BannerSite)
class BannerSiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_banner', 'published']


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.CommentProduct)
