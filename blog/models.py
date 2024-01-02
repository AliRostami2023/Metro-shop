from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.html import format_html
from account.models import User


# Create your models here.


class CategoryBlog(models.Model):
    title = models.CharField(max_length=300)
    url_title = models.CharField(max_length=350, unique=True, blank=True)
    image = models.ImageField(upload_to='uploads/blog_image', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,related_name='parent_category', null=True, blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-created']


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_blog')
    category = models.ManyToManyField(CategoryBlog, related_name='category')
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=550, blank=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='uploads/blog_image')
    date = models.DateField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    body = RichTextField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args={self.slug})

    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['-date']

