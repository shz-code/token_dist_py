# Generated by Django 4.1.5 on 2023-02-17 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0007_studentlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentlist',
            name='student_id',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='Student Id'),
        ),
    ]