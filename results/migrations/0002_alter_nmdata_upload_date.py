# Generated by Django 5.0.4 on 2024-10-06 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nmdata',
            name='upload_date',
            field=models.DateField(null=True),
        ),
    ]
