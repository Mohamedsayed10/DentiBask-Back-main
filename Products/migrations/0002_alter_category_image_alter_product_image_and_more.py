# Generated by Django 4.2.3 on 2023-11-10 08:58

import Products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=Products.models.unique_image_name),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=Products.models.unique_image_product),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
