# Generated by Django 3.2.4 on 2021-06-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_forgotpasswordtoken_verificationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgotpasswordtoken',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
