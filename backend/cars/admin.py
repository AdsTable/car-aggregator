from django.contrib import admin
from .models import Offer

# Register your models here.
class CarsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Offer, CarsAdmin)