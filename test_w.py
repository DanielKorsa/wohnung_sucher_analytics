#
import pprint
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from plotting import plot_bar_chart


TO_PRINT = []

munich_bezirke_print = [
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
    'Thal-Ober-Forsten-Fürst-Solln',
    'Hadern',
    'Pasing-Obermenzing',
    'Aubing-Lochhausen-Langwied',
    'Allach-Untermenzing',
    'Feldmoching-Hasenbergl',
    'Laim'
]

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

dataset = pd.read_csv('PANDAS_GEOCODED.csv', sep='\t', encoding='utf-8')
#! Delete wrong entries: Upper Bavaria, Oberbayern
dataset = dataset[dataset.cityDistrict.isin(munich_bezirke)]
#scams = dataset[dataset.price <700]

#print(dataset.info())
#print(scams.head(10))


def get_filtered_df_by(filter_value, column_name, dataset):
    '''
    Take column only with
    '''
    filtered_dataset = dataset[dataset[column_name] == filter_value]

    return filtered_dataset




# Get info about areas
avr_prices = []

inf_list = []

for district in munich_bezirke:

    inf = {}
    new_dataset = get_filtered_df_by(district, 'cityDistrict', dataset)
    avr_price = new_dataset['price'].mean()
    print('Averege price of a 2 room apartment in {} is {} euro'.format(district, "%.2f" % avr_price))
    avr_area = new_dataset['Area'].mean()
    print('Averege area of a 2 room apartment in {} is {} sq m'.format(district, "%.2f" % avr_area))
    avr_sqm_price = avr_price /avr_area
    print('Averege price in {} per sq m is {}'.format(district, "%.2f" % avr_sqm_price))
    print('\n')

    inf['district'] = district
    inf['price'] = "%.2f" % avr_price
    inf['avr_area'] = "%.2f" % avr_area
    inf['avr_sqm_price'] = "%.2f" % avr_sqm_price

    inf_list.append(inf)

pprint.pprint(inf_list)
dist_info = pd.DataFrame(inf_list)
dist_info.to_csv('district_price_info.csv', sep='\t', encoding='utf-8', index=False)


#! Printing
#plot_bar_chart(munich_bezirke_print, avr_prices, title= 'Price', ylabel= 'District')



if 'district_freq' in TO_PRINT:

    #! Print district distribution
    area_freq = dataset['cityDistrict'].value_counts()#.to_dict()
    area_freq.plot(kind='bar')
    plt.xticks(fontsize=8)
    plt.show()
    #pprint.pprint(area_freq)


def make_geojson_file(lats, langs, file_name = 'geo.geojson'):
    '''
    coords example = [11.63 , 48.16] lat , long
    '''

    geo_header = {"type": "FeatureCollection", "features": []}

    geojson_list = []

    for lat, lang in zip(lats,langs):

        single_geodata = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [lat, lang]
            }
        }
        geojson_list.append(single_geodata)

    geo_header['features'] = geojson_list
    #pprint.pprint(geo_header)

    with open('mygeo.geojson', 'w') as f:
        json.dump(geo_header, f)


# lats = dataset['lat'].to_list()
# langs = dataset['lang'].to_list()


# make_geojson_file(langs, lats)