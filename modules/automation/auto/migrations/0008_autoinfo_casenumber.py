# Generated by Django 3.2.18 on 2023-07-24 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0007_remove_autoinfo_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoinfo',
            name='casenumber',
            field=models.IntegerField(default=0, max_length=20, verbose_name='用例数量'),
        ),
    ]
