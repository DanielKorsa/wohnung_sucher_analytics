#
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



dataset = pd.read_csv('PANDAS_GEOCODED.csv', sep='\t', encoding='utf-8')


#scams = dataset[dataset.price <700]

#print(dataset.info())
#print(scams.head(10))


def get_filtered_df_by(filter_value, column_name, dataset):
    '''
    '''
    filtered_dataset = dataset[dataset[column_name] == filter_value]

    return filtered_dataset


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

for district in munich_bezirke:

    new_dataset = get_filtered_df_by(district, 'cityDistrict', dataset)
    avr_price = new_dataset['price'].mean()
    print('Averege price of a 2 room apartment in {} is {} euro'.format(district, "%.2f" % avr_price))
    avr_area = new_dataset['Area'].mean()
    print('Averege area of a 2 room apartment in {} is {} sq m'.format(district, "%.2f" % avr_area))

# print(new_dataset.info())
# print(new_dataset.head(3))