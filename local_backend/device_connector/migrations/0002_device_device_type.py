# Generated manually to add device_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_connector', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.CharField(default='ios', max_length=50),
        ),
    ]