# Generated by Django 3.2.18 on 2023-07-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0005_auto_20230719_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoinfo',
            name='update_time',
            field=models.DateTimeField(null=True, verbose_name='更新时间'),
        ),
    ]
