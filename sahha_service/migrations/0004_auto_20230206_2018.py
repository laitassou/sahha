# Generated by Django 3.2 on 2023-02-06 19:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sahha_service', '0003_annonces'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=250, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('country', 'city', 'name', 'address'),
            },
        ),
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('addresse', models.CharField(blank=True, default='', max_length=200)),
                ('gps_longitude', models.FloatField(null=True)),
                ('is_validated', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporting', models.TextField()),
                ('done', models.BooleanField(default=False)),
                ('gps_longitude', models.FloatField(null=True)),
                ('score', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('intervenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_periodic', models.BooleanField(default=False)),
                ('periodicity', models.SmallIntegerField(choices=[('Day', 'Day'), ('Week', 'Week')])),
                ('annonce_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sahha_service.annonce')),
                ('time_slot_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('annonce_id', 'start_time', 'end_time')},
            },
        ),
        migrations.DeleteModel(
            name='Annonces',
        ),
        migrations.AddField(
            model_name='intervention',
            name='slot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sahha_service.timeslot'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='based_category',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_id', to='sahha_service.categorie'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='based_location',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='sahha_service.agence'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='intervention',
            unique_together={('id', 'slot_id', 'intervenant')},
        ),
    ]