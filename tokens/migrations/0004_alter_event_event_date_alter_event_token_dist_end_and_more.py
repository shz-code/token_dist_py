# Generated by Django 4.1.5 on 2023-02-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0003_event_token_dist_end_event_token_dist_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='token_dist_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Token Distribution End'),
        ),
        migrations.AlterField(
            model_name='event',
            name='token_dist_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Token Distribution Start'),
        ),
    ]
