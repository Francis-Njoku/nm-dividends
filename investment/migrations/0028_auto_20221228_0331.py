# Generated by Django 3.2.16 on 2022-12-28 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0027_investment_offer_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='annualized',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='investment',
            name='roi',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
