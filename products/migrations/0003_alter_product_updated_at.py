# Generated by Django 5.0.4 on 2024-04-10 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
