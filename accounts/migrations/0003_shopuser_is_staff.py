# Generated by Django 3.0.6 on 2020-05-17 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200517_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='staff'),
        ),
    ]