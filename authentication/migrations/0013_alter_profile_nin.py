# Generated by Django 3.2.16 on 2023-02-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nin',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
