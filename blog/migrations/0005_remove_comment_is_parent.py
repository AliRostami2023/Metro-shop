# Generated by Django 5.0 on 2024-01-17 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_parent',
        ),
    ]
