from django.db import models

# Create your models here.


class ContactUs(models.Model):
    full_name = models.CharField(max_length=350)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=70)
    subject = models.CharField(max_length=350)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contact us'
        ordering = ['-created']


