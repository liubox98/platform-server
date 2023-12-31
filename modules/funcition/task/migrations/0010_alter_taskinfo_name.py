# Generated by Django 3.2.18 on 2023-06-09 08:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_alter_taskinfo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskEventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=255)),
                ('task', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('operator', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'task_event_log',
            },
        ),
    ]
