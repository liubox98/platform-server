# Generated by Django 3.2.18 on 2023-07-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0004_alter_autoinfo_performer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autoinfo',
            name='url',
        ),
        migrations.AlterField(
            model_name='autoinfo',
            name='status',
            field=models.CharField(default='进行中', max_length=255, verbose_name='状态'),
        ),
    ]
