# Generated by Django 5.0 on 2024-01-19 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_category_is_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_parent',
            field=models.BooleanField(default=False),
        ),
    ]
