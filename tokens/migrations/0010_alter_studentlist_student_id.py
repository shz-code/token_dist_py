# Generated by Django 4.1.5 on 2023-02-17 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0009_studentlist_claimed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentlist',
            name='student_id',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Student Id'),
        ),
    ]
