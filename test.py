


# import pprint
# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="testmunich")
# #location = geolocator.reverse("48.8588443, 2.2943506")
# #print(location.address)

# location = geolocator.geocode('Schleissheimerstr 14, Munich')

# pprint.pprint(location.raw)


# #Types: political, sublocality, sublocality_level_1


# Read clean addresses

def read_addresses_txt(file_name):

    adrss = []

    with open(file_name, 'r') as f:
        a = f.readlines()
        adrss.append(a)




