# Generated by Django 4.2.3 on 2023-11-17 11:27

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=User.models.unique_image_customer),
        ),
    ]
