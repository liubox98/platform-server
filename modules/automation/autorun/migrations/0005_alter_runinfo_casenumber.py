# Generated by Django 3.2.18 on 2023-07-24 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorun', '0004_runinfo_casenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runinfo',
            name='casenumber',
            field=models.IntegerField(default=0, verbose_name='用例数量'),
        ),
    ]
