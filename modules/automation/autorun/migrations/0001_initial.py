# Generated by Django 3.2.18 on 2023-07-19 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auto', '0007_remove_autoinfo_update_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='任务名')),
                ('modules', models.CharField(max_length=255, verbose_name='模块名')),
                ('executor', models.CharField(max_length=255, verbose_name='执行人')),
                ('maintain', models.CharField(max_length=255, verbose_name='维护人')),
                ('report', models.URLField(verbose_name='报告')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='状态')),
                ('task_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='auto.autoinfo')),
            ],
        ),
    ]
