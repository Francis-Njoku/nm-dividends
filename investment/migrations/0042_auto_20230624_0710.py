# Generated by Django 3.1.1 on 2023-06-24 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0041_investment_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='payment',
        ),
        migrations.AddField(
            model_name='investors',
            name='payment',
            field=models.CharField(choices=[('not started', 'not started'), ('partial', 'partial'), ('full', 'full')], default='not started', max_length=255),
        ),
    ]
