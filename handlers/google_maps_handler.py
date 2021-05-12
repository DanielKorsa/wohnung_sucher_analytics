#
import pprint
import configparser
import googlemaps
import json


CONF_FILE = 'config.ini'

def read_ini_file(file_name, key1, key2):
    '''
    '''
    config = configparser.ConfigParser()
    config.read(file_name)

    return config.get(key1, key2)


def g_maps_auth(api_key):
    '''
    '''
    CONF_FILE = 'config.ini'
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    api_key = config.get('TOKENS','GMAPIKEY')

    return googlemaps.Client(key=api_key)

def geocode_address(gmaps_ref, address):
    '''
    out type - list
    '''
    try:
        full_info = gmaps_ref.geocode(address)

    except:
        print('Could not geocode address: {}'.format(address))
        full_info = [] # return an empty list on error

    return full_info

def unpack_geocoded_data(geocoded_data):
    '''
    Unpack google maps api returned msg
    '''
    try:
        city_dist = geocoded_data[0]['address_components'][2]['long_name'] # get city district
    except:
        try:
            city_dist = geocoded_data[0]['address_components'][2]['short_name'] # get city district
        except:
            city_dist = 'Nan'
            print('could not get city district')

    lat = geocoded_data[0]['geometry']['location']['lat'] # get lattitude
    lang = geocoded_data[0]['geometry']['location']['lng']# get langitude

    return city_dist, lat, lang



# #! TEST
# ADDRESS = 'Georgenstraße 35, 80799 München, Universität'
# TEST_GEOCODED_DATA = [{
#     'address_components': [{
#         'long_name': '35',
#         'short_name': '35',
#         'types': ['street_number']
#     }, {
#         'long_name': 'Georgenstraße',
#         'short_name': 'Georgenstraße',
#         'types': ['route']
#     }, {
#         'long_name':
#         'Maxvorstadt',
#         'short_name':
#         'Maxvorstadt',
#         'types': ['political', 'sublocality', 'sublocality_level_1']
#     }, {
#         'long_name': 'München',
#         'short_name': 'München',
#         'types': ['locality', 'political']
#     }, {
#         'long_name':
#         'Oberbayern',
#         'short_name':
#         'Oberbayern',
#         'types': ['administrative_area_level_2', 'political']
#     }, {
#         'long_name':
#         'Bayern',
#         'short_name':
#         'BY',
#         'types': ['administrative_area_level_1', 'political']
#     }, {
#         'long_name': 'Germany',
#         'short_name': 'DE',
#         'types': ['country', 'political']
#     }, {
#         'long_name': '80799',
#         'short_name': '80799',
#         'types': ['postal_code']
#     }],
#     'formatted_address':
#     'Georgenstraße 35, 80799 München, Germany',
#     'geometry': {
#         'location': {
#             'lat': 48.1549144,
#             'lng': 11.5762798
#         },
#         'location_type': 'ROOFTOP',
#         'viewport': {
#             'northeast': {
#                 'lat': 48.15626338029149,
#                 'lng': 11.5776287802915
#             },
#             'southwest': {
#                 'lat': 48.1535654197085,
#                 'lng': 11.5749308197085
#             }
#         }
#     },
#     'partial_match':
#     True,
#     'place_id':
#     'ChIJtU7__MF1nkcR7hPfTj2WA1s',
#     'plus_code': {
#         'compound_code': '5H3G+XG Munich, Germany',
#         'global_code': '8FWH5H3G+XG'
#     },
#     'types': ['street_address']
# }]

# api_key = read_ini_file(CONF_FILE, 'TOKENS', 'GMAPIKEY')
# gmaps_ref = g_maps_auth(api_key)
# geocoded_data = geocode_address(gmaps_ref, ADDRESS)
# city_dist, lat, lang = unpack_geocoded_data(geocoded_data)

