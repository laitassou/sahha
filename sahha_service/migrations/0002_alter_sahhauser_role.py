# Generated by Django 3.2 on 2023-01-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sahha_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sahhauser',
            name='role',
            field=models.CharField(choices=[('Worker', 'Worker'), ('Client', 'Client'), ('Manager', 'Manager'), ('Supervisor', 'Supervisor')], default='Worker', max_length=120),
        ),
    ]
