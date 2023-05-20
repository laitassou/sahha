# Generated by Django 3.2 on 2023-02-19 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sahha_service', '0009_remove_timeslot_time_slot_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='time_slot_intervenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]