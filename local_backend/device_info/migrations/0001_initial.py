# Generated by Django 3.2.25 on 2025-04-13 14:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255, unique=True)),
                ('ios_version', models.CharField(blank=True, max_length=50, null=True)),
                ('model_identifier', models.CharField(blank=True, max_length=50, null=True)),
                ('battery_level', models.IntegerField(blank=True, null=True)),
                ('storage_total', models.BigIntegerField(blank=True, null=True)),
                ('storage_used', models.BigIntegerField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
