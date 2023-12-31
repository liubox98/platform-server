# Generated by Django 3.2.16 on 2023-06-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommitInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commit_hash', models.CharField(max_length=50, verbose_name='提交hash值')),
                ('version', models.CharField(max_length=50, verbose_name='提交版本')),
                ('confire', models.BooleanField(default=False, verbose_name='是否确认合并')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
