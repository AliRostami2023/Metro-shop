from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/avatar_user', null=True, blank=True)
    email_active_code = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['-id']
        verbose_name = 'user'
        verbose_name_plural = 'users'
