import scale_ai_map


location_map = { 'A-basin': 'ChIJWd2U7rRQaocRllxVIFIp5Ts',
 'Jackson Hole Mountain Resort': 'ChIJeWipzkIaU1MROB6YO554dn8',
 'Kirkwood Mountain Resort': 'ChIJyw_jRk3xmYARn-W118rvXYs',
 'Palisades Tahoe': 'ChIJPSaP8OzZm4ARDxeFl_CIvjA'
 }

origin_1 = location_map['A-basin']
destination_1 = location_map['Jackson Hole Mountain Resort']

scale_ai_map.get_travel_time(origin_1, destination_1)


#'Invalid JSON payload received. Unknown name "origin": Cannot bind query parameter. \'origin\' is a message type. 
# Parameters can only be bound to primitive types.
# \nInvalid JSON payload received. 
# Unknown name "destination": Cannot bind query parameter. 
# \'destination\' is a message type. Parameters can only be bound to primitive types.'
