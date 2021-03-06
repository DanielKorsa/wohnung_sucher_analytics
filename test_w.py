#
import pprint
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from plotting import plot_bar_chart, plot_bar_chart_dists


TO_PRINT = ['district_avr_price']

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

dataset = pd.read_csv('PANDAS_GEOCODED_LAST.csv', sep='\t', encoding='utf-8')
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

FONT = {'fontname':'Arial'}
TITLE_S = 27
LABEL_S = 23

if 'district_avr_price' in TO_PRINT:

    # Get info about areas
    avr_prices = []
    clean_price_dataset = dataset[~(dataset['price'] < 600)] 
    for district in munich_bezirke:
        
        new_dataset = get_filtered_df_by(district, 'cityDistrict', clean_price_dataset)
        avr_price = new_dataset['price'].mean()
        avr_prices.append(avr_price)
        print('Averege price of a 2 room apartment in {} is {} euro'.format(district, "%.2f" % avr_price))
        avr_area = new_dataset['Area'].mean()
        print('Averege area of a 2 room apartment in {} is {} sq m'.format(district, "%.2f" % avr_area))


    plot_bar_chart_dists(munich_bezirke_print, avr_prices, title= 'Averege price per district', ylabel= 'Price, €', bar_color = '#F3A0F2')


if 'district_freq' in TO_PRINT:

    #! Print district distribution
    area_freq = dataset['cityDistrict'].value_counts()
    area_freq.plot(kind='bar')
    plt.ylabel('Number of listings',fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.title('Flat listings per area', fontsize=TITLE_S, pad=30, style='italic', **FONT)
    plt.bar(range(len(area_freq)), area_freq, color='#661D98')
    plt.xticks(fontsize=19, **FONT)
    plt.yticks(fontsize=19, **FONT)
    plt.show()
    


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

#! Creating GEOJSON File
# lats = dataset['lat'].to_list()
# langs = dataset['lang'].to_list()


# make_geojson_file(langs, lats)