# Generated by Django 5.0 on 2024-01-19 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_commentproduct_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_parent',
            field=models.BooleanField(default=True),
        ),
    ]
