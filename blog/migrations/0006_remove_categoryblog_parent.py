# Generated by Django 5.0 on 2024-12-07 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_comment_is_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryblog',
            name='parent',
        ),
    ]