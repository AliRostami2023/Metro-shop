from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from account.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=300)
    url_title = models.CharField(max_length=330, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='category_parent')
    is_parent = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/category_image', null=True, blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-created']


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='category', blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='brand')
    title = models.CharField(max_length=450)
    slug = models.SlugField(max_length=500, unique=True, allow_unicode=True, blank=True)
    image = models.ImageField(upload_to='uploads/product_images')
    price = models.IntegerField()
    discount = models.SmallIntegerField(null=True, blank=True)
    color = models.ManyToManyField('Color', related_name='colors')
    size = models.ManyToManyField('Size', related_name='sizes')
    availability = models.SmallIntegerField(null=True, blank=True)
    short_body = RichTextField(max_length=400)
    body = RichTextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    rating = GenericRelation(Rating, related_name='rating_product')

    def __str__(self):
        return f"{self.title} - {self.price}"

    @property
    def result_total_price(self):
        if not self.discount:
            return self.price
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        return self.price

        return self.total_price

    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created']


class ImagesProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/images_products')

    def __str__(self):
        return self.product.title

    def image_other(self):
        return format_html('<img src = "{}" width=60% height=90px>'.format(self.image.url))


class Brand(models.Model):
    title = models.CharField(max_length=300)
    url_title = models.CharField(max_length=350, unique=True, blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['-created']


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'sizes'


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'colors'


class Slider(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='uploads/slider')
    url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def image_slide(self):
        return format_html('<img src = "{}" width=22% height=70px>'.format(self.image.url))

    class Meta:
        verbose_name = 'slider'
        verbose_name_plural = 'sliders'


class BannerSite(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/banners')
    url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def image_banner(self):
        return format_html('<img src = "{}" width=22% height=70px>'.format(self.image.url))

    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'


class CommentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_product')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.user} - {self.body[:20]}"

    class Meta:
        verbose_name_plural = 'comments'
        ordering = ['-created']

