# Generated by Django 3.2.18 on 2023-07-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0008_autoinfo_casenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoinfo',
            name='casenumber',
            field=models.IntegerField(default=0, verbose_name='用例数量'),
        ),
    ]
