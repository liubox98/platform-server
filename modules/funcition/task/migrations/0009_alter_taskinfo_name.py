# Generated by Django 3.2.18 on 2023-04-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_alter_taskinfo_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinfo',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
