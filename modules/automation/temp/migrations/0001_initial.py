# Generated by Django 3.2.18 on 2023-07-24 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modules', models.CharField(max_length=255, verbose_name='任务名')),
                ('number', models.IntegerField(default=0, verbose_name='数量')),
            ],
        ),
    ]
