# Generated by Django 4.1.5 on 2023-02-12 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Phone'),
        ),
    ]
