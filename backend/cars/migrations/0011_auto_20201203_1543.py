# Generated by Django 3.1.3 on 2020-12-03 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0010_offer_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='offerId',
            field=models.IntegerField(),
        ),
    ]