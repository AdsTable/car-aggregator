from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Offer(models.Model):
    offerId = models.IntegerField()
    iaaiId = models.IntegerField(unique=True, null=True)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    production_year = models.IntegerField()
    mileage = models.IntegerField(null=True)
    primary_damage = models.CharField(max_length=50, null=True)
    secondary_damage = models.CharField(max_length=50, null=True)
    estimated_retail_value = models.IntegerField(null=True)
    estimated_repair_cost = models.DecimalField(decimal_places=2, max_digits=10, null=True)
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
    thumb_image = models.URLField(max_length=500, null=True)
    images = ArrayField(models.URLField(), null=True)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    auction_site = models.CharField(default="copart", max_length=20)
    loss_type = models.CharField(max_length=30, null=True)
    buy_now = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    closed = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('offerId', 'auction_site')
        ordering = ['-id']

    def __str__(self):
        return f"{self.brand} {self.model} | {self.offerId}"


