from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Offer(models.Model):
    offerId = models.IntegerField(unique=True)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    production_year = models.IntegerField()
    mileage = models.IntegerField(null=True)
    primary_damage = models.CharField(max_length=50, null=True)
    secondary_damage = models.CharField(max_length=50, null=True)
    estimated_retail_value = models.IntegerField(null=True)
    vin = models.CharField(max_length=17, null=True)
    drive = models.CharField(max_length=30, null=True)
    body_style = models.CharField(max_length=30, null=True)
    vehicle_type = models.CharField(max_length=30, null=True)
    fuel = models.CharField(max_length=30, null=True)
    engine = models.CharField(max_length=30, null=True)
    transmission = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=70, null=True)
    sale_date = models.DateTimeField(null=True)
    sold = models.BooleanField(default=False)
    images = ArrayField(models.URLField(), null=True)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    auction_site = models.CharField(default="copart", max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} | {self.offerId}"


