from django.db.models import F, Count

from cars.models import Offer


def get_available_options_for_field(field):
    options = list(Offer.objects.values_list(field, flat=True).distinct().order_by(field))
    return list(filter(None, options))


def get_brand_for_type(vehicle_type):
    models = list(
        Offer.objects.filter(vehicle_type=vehicle_type).values_list('brand', flat=True).distinct().order_by('brand'))
    return list(filter(None, models))


def get_models_for_brand(car_type, brand):
    # TODO: REFACTOR THIS IF ELSE LOGIC
    if car_type and brand:
        models = list(Offer.objects.filter(brand=brand, vehicle_type=car_type).values_list('model',
                                                                                           flat=True).distinct().order_by(
            'model'))
    elif car_type and not brand:
        models = list(
            Offer.objects.filter(vehicle_type=car_type).values_list('model', flat=True).distinct().order_by('model'))
    elif not car_type and brand:
        models = list(
            Offer.objects.filter(brand=brand).values_list('model', flat=True).distinct().order_by('model'))
    else:
        models = list(
            Offer.objects.values_list('model', flat=True).distinct().order_by('model'))
    return list(filter(None, models))
