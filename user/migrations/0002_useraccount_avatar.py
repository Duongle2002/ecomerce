# Generated by Django 5.0.4 on 2024-04-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='avatar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
