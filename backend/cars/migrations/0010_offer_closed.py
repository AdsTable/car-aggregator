# Generated by Django 3.1.3 on 2020-12-03 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_offer_thumb_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
