# Generated by Django 3.2.18 on 2023-07-25 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0009_alter_autoinfo_casenumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autoinfo',
            old_name='casenumber',
            new_name='number',
        ),
    ]
