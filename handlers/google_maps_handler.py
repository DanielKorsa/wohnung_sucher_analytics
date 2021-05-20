#
import pprint
import configparser
import googlemaps
import json


CONF_FILE = 'config.ini'

def read_ini_file(file_name, key1, key2):
    """[Read .ini file]

    Args:
        file_name ([str]): [path to ini file]
        key1 ([str]): [first key]
        key2 ([str]): [second key]

    Returns:
        [str]: [description]
    """
    config = configparser.ConfigParser()
    config.read(file_name)

    return config.get(key1, key2)


def g_maps_auth(api_key):
    """[Auth for google maps]

    Args:
        api_key ([str]): [api key]

    Returns:
        [type]: [description]
    """
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    api_key = config.get('TOKENS','GMAPIKEY')

    return googlemaps.Client(key=api_key)

def geocode_address(gmaps_ref, address):
    """[Geocode an address]

    Args:
        gmaps_ref ([type]): [description]
        address ([str]): [description]

    Returns:
        [list]: [geocoded data]
    """
    try:
        full_info = gmaps_ref.geocode(address)

    except:
        print('Could not geocode address: {}'.format(address))
        full_info = [] # return an empty list on error

    return full_info

def unpack_geocoded_data(geocoded_data):
    """[Unpack google maps api returned msg.]

    Args:
        geocoded_data ([type]): [Example can be found in docs]

    Returns:
        [type]: [district, lattitude, longitude]
    """
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

