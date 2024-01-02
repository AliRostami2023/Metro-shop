# Generated by Django 5.0 on 2023-12-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'colors',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'sizes',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(related_name='colors', to='product.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(related_name='sizes', to='product.size'),
        ),
    ]
