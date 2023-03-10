# Generated by Django 4.1.5 on 2023-02-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0010_alter_studentlist_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tags',
        ),
        migrations.AddField(
            model_name='token',
            name='entry_flag',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Entery Status'),
        ),
        migrations.AddField(
            model_name='token',
            name='food_flag',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Food Status'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
