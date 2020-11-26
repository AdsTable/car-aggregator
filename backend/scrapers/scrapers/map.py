def map_drive(value):
    if value == '4x4 w/Front Whl Drv':
        return '4x4 Front Wheel Drive'
    if value == '4x4 w/Rear Wheel Drv':
        return '4x4 Rear Wheel Drive'
    if value == 'All wheel drive':
        return 'All Wheel Drive'
    if value in ['Front wheel drive', 'Front-wheel drive']:
        return 'Front Wheel Drive'
    if value == 'Rear-wheel drive':
        return 'Rear Wheel Drive'
    return value

def map_body(value):
    if value: 
        value = value.upper()
    else:
        return ''
    if value.startswith('WAGON 4'):
        return 'WAGON 4 DOOR'
    if value.startswith('WAGON 2'):
        return 'WAGON 2 DOOR'
    if value.startswith('SPORT UTILITY'):
        return 'SPORT UTILITY VEHICLE'
    if value.startswith('SPORT V'):
        return 'SPORT VAN'
    if value.startswith('SPORT PI'):
        return 'SPORT PICKUP'
    if value.startswith('SEDAN 4'):
        return 'SEDAN 4 DOOR'
    if value.startswith('SEDAN 2'):
        return 'SEDAN 2 DOOR'
    if value.startswith('ROAD'):
        return 'ROADSTER'
    if value.startswith('HATCHBACK 4'):
        return 'HATCHBACK 4 DOOR'
    if value.startswith('HATCHBACK 2'):
        return 'HATCHBACK 2 DOOR'
    if value == 'HATCHBAC':
        return 'HATCHBACK'
    if value.startswith('CREW PI'):
        return 'CREW PICKUP'
    if value.startswith('CREW CHA'):
        return 'CREW CHASSIS'
    if value.endswith('DR.'):
        return value.replace('DR.', 'DOOR')
    if value == 'CONVERTI':
        return 'CONVERTIBLE'
    if value == 'CONVENTI':
        return 'CONVENTIONAL'
    if value == 'CARGO VA':
        return 'CARGO VAN'
    return value
    
def map_damage(value):
    if value: 
        value = value.upper()
    else:
        return ''
    if value == "VANDALISM":
        return 'VANDALIZED'
    if value == "STRIP":
        return "STRIPPED"
    if value == "REAR":
        return "REAR END"
    if value == "FRAME":
        return "FRAME DAMAGE"
    if value == "TOTAL BURN":
        return "BURN"
    if value == "BIO HAZARD":
        return "BIOHAZARD/CHEMICAL"
    return value

def map_fuel(value):
    if value: 
        value = value.upper()
    else:
        return ''
    if value in ['OTHER', 'UNKNOWN', 'X']:
        return 'UNKNOWN'
    if value in ['COMPRESSED NATURAL GAS', 'GAS']:
        return 'GASOLINE'
    return value

    
    