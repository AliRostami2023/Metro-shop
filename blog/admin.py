from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'image_tag', 'date', 'published']
    list_filter = ['published']
    search_fields = ['author', 'title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.CategoryBlog)
class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'published']
    prepopulated_fields = {'url_title': ('title',)}
