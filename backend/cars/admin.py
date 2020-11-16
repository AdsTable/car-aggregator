from django.contrib import admin
from .models import Offer

# Register your models here.
@admin.register(Offer)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('offerId', 'brand', 'model', 'vin', 'production_year', 'sold', 'sale_date', 'created_at', 'updated_at')
    list_filter = ('sold', 'sale_date', 'created_at')
    search_fields = ('brand', 'model')
    date_hierarchy = 'sale_date'

    
