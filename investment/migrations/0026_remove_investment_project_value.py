# Generated by Django 3.2.16 on 2022-12-23 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0025_auto_20221223_0707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='project_value',
        ),
    ]
