# Generated by Django 3.2.4 on 2021-06-11 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210610_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forgotpasswordtoken',
            name='verified',
        ),
    ]
