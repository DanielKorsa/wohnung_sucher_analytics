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


list_of_addrs = read_addresses_txt('clean_addresses.txt')
price_list = read_addresses_txt('clean_prices.txt')

#geocode_all_addresses(list_of_addrs) #! Use Google maps 

def read_json_file(file_name):

    with open(file_name, 'r') as f:
        result = json.load(f)
    return(result)

def get_city_areas(json_list):
    all_areas = []
    for info in json_list:

        all_areas.append(info['address_components'][2]['long_name'])
        

    return all_areas


all_geodata = read_json_file('geodata_test.json') #! Get all geodata from json
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
#pprint.pprint(sorted_areas) #! Printing how many times per area


MARIENPLATZ_COORD = [48.1374, 11.5754]
long_and_latitudes = [48.1500873802915, 11.5607710802915]


from math import sin, cos, sqrt, atan2, radians
def calc_dist_from_long_lat(point_one, point_two):
    
    R = 6373.0
    
    dlon = radians(point_two[1]) - radians(point_one[1])
    dlat = radians(point_two[0]) - radians(point_one[0])


    a = sin(dlat / 2)**2 + cos(point_one[0]) * cos(point_two[0]) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance



lats_lons = []
km_distances = []

for coords in all_geodata:

    predata = ((coords['geometry']['viewport']['northeast']))
    lat_long = [predata['lat'], predata['lng']]
    lats_lons.append(lat_long)
    km_distances.append(calc_dist_from_long_lat(MARIENPLATZ_COORD, lat_long))

#pprint.pprint(km_distances)
#pprint.pprint(price_list)
print(len(price_list))
print(len(km_distances))
# km_distance = calc_dist_from_long_lat(MARIENPLATZ_COORD, long_and_latitudes)
# print(km_distance)

price_list_int = [int(i) for i in price_list]

import matplotlib.pyplot as plt
import pandas as pd
# Create a dataset:
df=pd.DataFrame({'distance': km_distances[:657], 'price': price_list_int})

# plot
plt.plot( 'distance', 'price', data=df, linestyle='none', marker='o')
plt.show()


plt.plot(km_distances[:657], price_list_int)
plt.show()











# # import the library
# import folium
# import pandas as pd
 
# # Make a data frame with dots to show on the map
# data = pd.DataFrame({
#    'lat':[-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
#    'lon':[-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
#    'name':['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg', 'Abidjan', 'Montreal', 'Nairobi', 'Salvador'],
#    'value':[10,12,40,70,23,43,100,43]
# })

 
# # Make an empty map
# m = folium.Map(location=[20,0], tiles="Mapbox Bright", zoom_start=2)
 
# # I can add marker one by one on the map
# for i in range(0,len(data)):
#    folium.Circle(
#       location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
#       popup=data.iloc[i]['name'],
#       radius=data.iloc[i]['value']*10000,
#       color='crimson',
#       fill=True,
#       fill_color='crimson'
#    ).add_to(m)
 
# # Save it as html
# m.save('mymap.html')