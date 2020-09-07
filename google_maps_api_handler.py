#
import pprint
import configparser
import googlemaps
import json



CONF_FILE = 'config.ini'
config = configparser.ConfigParser()                                     
config.read(CONF_FILE)
api_key = config.get('TOKENS','GMAPIKEY')
gmaps = googlemaps.Client(key=api_key)


def geocode_all_addresses(addresses_list):
    '''
    Geocodes a list of addresses and saves it as a json file
    '''
    geocode_result_json_list = []
    i = 0
    # Geocoding an address
    for address in addresses_list:

        i+=1
        print(i)
        
        try:
            geocode_result = gmaps.geocode(address)
            geocode_result_json_list.append(geocode_result[0])
        except:
            print('Error in geocoding')
            

    with open('geodata_test.json', 'w') as fout:
        json.dump(geocode_result_json_list, fout)

def read_addresses_txt(file_name):

    return open(file_name).read().splitlines()


#list_of_addrs = read_addresses_txt('clean_addresses.txt')

#geocode_all_addresses(list_of_addrs)

def read_json_file(file_name):

    with open(file_name, 'r') as f:
        result = json.load(f)
    return(result)

def get_city_areas(json_list):
    all_areas = []
    for info in json_list:

        all_areas.append(info['address_components'][2]['long_name'])
        

    return all_areas


all_geodata = read_json_file('geodata_test.json')
#areas = get_city_areas(all_geodata)




munich_bezirke = [
    'Altstadt-Lehel',
    'Ludwigsvorstadt-Isarvorstadt',
    'Maxvorstadt',
    'Schwabing-West',
    'Au-Haidhausen',
    'Sendling',
    'Sendling-Westpark',
    'Schwanthalerhöhe',
    'Neuhausen-Nymphenburg',
    'Moosach',
    'Milbertshofen-Am Hart',
    'Schwabing-Freimann',
    'Bogenhausen',
    'Berg am Laim',
    'Trudering-Riem',
    'Ramersdorf-Perlach',
    'Obergiesing-Fasangarten',
    'Untergiesing-Harlaching',
    'Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln',
    'Hadern',
    'Pasing-Obermenzing',
    'Aubing-Lochhausen-Langwied',
    'Allach-Untermenzing',
    'Feldmoching-Hasenbergl',
    'Laim'
]


found_bezirks = []

for area in all_geodata:
    
    for bezirk in munich_bezirke:
        if bezirk in str(area['address_components']):
            found_bezirks.append(bezirk)
        else:
            pass


#pprint.pprint(found_bezirks)

from collections import Counter

sorted_areas = Counter(found_bezirks)
pprint.pprint(sorted_areas)
#print(type(all_geodata[1]))