# Generated by Django 3.2.16 on 2022-12-04 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='message',
            new_name='comment',
        ),
    ]
