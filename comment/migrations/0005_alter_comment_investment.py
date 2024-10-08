# Generated by Django 3.2.16 on 2023-01-15 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0029_investment_periodic_payment'),
        ('comment', '0004_auto_20230115_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='investment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments_comment', to='investment.investment'),
        ),
    ]
