# Generated by Django 3.2 on 2023-02-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sahha_service', '0005_auto_20230206_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]