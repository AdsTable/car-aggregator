# Generated by Django 3.1.3 on 2020-11-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_offer_iaaiid'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='buy_now',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='estimated_repair_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='loss_type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]