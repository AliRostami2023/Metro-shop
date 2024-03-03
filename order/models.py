from django.db import models

from account.models import User
from product.models import Product


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    is_paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    track_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()}-{self.first_name}-{self.is_paid}"

    @property
    def result_total_price(self):
        total_amount = 0
        for order_detail in self.order_items.all():
            total_amount += order_detail.product.result_total_price * order_detail.quantity
        return total_amount

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_item')
    size = models.CharField(max_length=12)
    color = models.CharField(max_length=12)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
