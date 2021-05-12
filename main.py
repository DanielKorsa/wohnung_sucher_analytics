#
import pprint
from numpy.lib.arraypad import pad
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
from handlers.db_handler import dynamodb_connect, scan_db
from handlers.data_handler import (
    clean_price,
    clean_online_since_date,
    clean_online_since_time,
    clean_description,
    clean_address_data,
    weekly_freq_prep,
    daily_freq_prep,
    pet_info_prep
    )

from handlers.plot_handler import (
    plot_bar_chart,
    plot_histogram,
    plot_pie_chart
    )

#from plotting import #plot_wordcloud #? New version of wordcloud needs MVS 14.0 +
from handlers.google_maps_handler import (
    geocode_address,
    read_ini_file,
    g_maps_auth,
    unpack_geocoded_data
    )

CONF_FILE = 'config.ini'
UPDATE_DB = False # Use AWS/Local data
CLEAN_DATA = False # Clean data y/n?
GOOGLE_GEOCODE = False # Use Google Geocoding/local ge data
PRINT = True # Print values
VIZ = {'text_info': True,
        'price_hist': True,
        'weekly_dist': False,
        'daily_dist': False,
        'pet_data': False,
        'wordcloud': False,
        'area_price': False
        }

if UPDATE_DB:
    '''
    Get fresh dataset from AWS DynamoDB
    '''
    db_instance = dynamodb_connect('wohnung_sucher_db')
    db_full_content = scan_db(db_instance,'source', 'immoscout24')
    dataset = pd.DataFrame(db_full_content)
    # Save dataset to .csv
    #dataset.to_csv('PANDAS_CSV.csv', sep='\t', encoding='utf-8', index=False)

else:
    '''
    Get local CLEAN copy of dataset
    '''
    dataset = pd.read_csv('PANDAS_GEOCODED.csv', sep='\t', encoding='utf-8')

if CLEAN_DATA:
    # Cleaning data
    columns_to_drop = ['email', 'phone', 'source'] # Remove columns which are not used
    dataset.drop(columns_to_drop, inplace=True, axis=1)

    dataset['Area'] = dataset['Area'].apply(lambda area: float(area.split(' ')[0].replace(',','.'))) # clean Area data
    dataset['price'] = dataset['price'].apply(clean_price) # Clean price from . ,
    dataset['petsAllowed'] = dataset['petsAllowed'].fillna(value='Not Specified') # Fill PetsAllowed NaN with Nach Vereinbarung
    dataset['onlineSinceDate'] = dataset['onlineSince'].apply(clean_online_since_date)
    dataset['onlineSinceTime'] = dataset['onlineSince'].apply(clean_online_since_time)
    dataset['formattedAddress'] = dataset['address'].apply(clean_address_data)
    dataset.drop('onlineSince', inplace=True, axis=1) #TODO cheeck why index shifts
    #! write clean data to csv
    dataset.to_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8', index=False)

if GOOGLE_GEOCODE:
    # Use Google Cloud to geocode data
    api_key = read_ini_file(CONF_FILE, 'TOKENS', 'GMAPIKEY')
    gmaps_ref = g_maps_auth(api_key)
    city_dist_list = []
    lat_list = []
    lang_list = []

    addresses = dataset['formattedAddress'].tolist()
    for address in addresses:
        #print(address)
        geocoded_data = geocode_address(gmaps_ref, address)
        city_dist, lat, lang = unpack_geocoded_data(geocoded_data)
        city_dist_list.append(city_dist)
        lat_list.append(lat)
        lang_list.append(lang)

    # Add geocoded data to dataset
    dataset['cityDistrict'] = city_dist_list
    dataset['lat'] = lat_list
    dataset['lang'] = lang_list

    # Write dataset to .csv
    dataset.to_csv('PANDAS_GEOCODED.csv', sep='\t', encoding='utf-8', index=False)

#! PRINTING & PLOTTING
if PRINT:

    if VIZ['text_info']:
        # Print analyzed text data
        avr_area = dataset['Area'].mean()
        print('Averege area of a 2 room apartment in Munich is {} sq m'.format("%.2f" % avr_area))

        avr_price = dataset['price'].mean()
        print('Averege price of a 2 room apartment in Munich is {} euro'.format("%.2f" % avr_price))

        no_address = dataset['formattedAddress'].apply(lambda only_post: only_post.split(' ')[0].isdigit())
        falses, trues = no_address.value_counts().to_list() # trues = full address is not provided
        no_address_perc = (trues / (falses + trues)) * 100
        print('Only {} percent of ads reveal the real address'.format("%.1f" % no_address_perc))

    if VIZ['price_hist']:
        # Plot price histogram
        dataset['price'].plot(kind='density')
        plt.ylabel('Density',fontsize=15)
        plt.xlabel('Price, €',fontsize=15, labelpad=20)
        plt.title('Averege price distribution',fontsize=15, pad=30)
        plt.xticks(fontsize=12)
        plt.tick_params(axis='x', which='major', pad=10)
        plt.yticks(fontsize=5)
        plt.show()

    if VIZ['weekly_dist']:
        # Plot weekly distribution graph
        weekday_title = 'Weekly apartment listing distribution'
        weekday_ylabel = 'Apartment listings per week'
        weekday_data, weekday_objects = weekly_freq_prep(dataset['onlineSinceDate'])
        chart_week_dist = plot_bar_chart(weekday_objects, weekday_data, title=weekday_title, ylabel=weekday_ylabel)

    if VIZ['daily_dist']:
        # Plot daily distribution graph
        hour_title = 'Weekly apartment listing distribution'
        hourly_freq = daily_freq_prep(dataset['onlineSinceTime'])
        chart_hour_dist = plot_histogram(data=hourly_freq,title=hour_title, n_bins=24)

    if VIZ['pet_data']:
        # Plot bar chat - pet allowed/not data
        pet_data_dist, pets_labels = pet_info_prep(dataset['petsAllowed'])
        pets_labels = ['No', 'Yes', 'Not specified', 'By arrangement']
        chart_pie = plot_pie_chart(pet_data_dist, pets_labels)

    if VIZ['wordcloud']:
        # Print world cloud
        clean_descriptions = clean_description(dataset['description'])
        # Generate word cloud
        my_stopwords_list = [
            'mit', 'zi', 'im', 'voll', 'whg', 'und', 'von', 'der', 'die',
            'nach', 'ab', 'uhr', 'um', 'zum', 'für', 'whg', 'eg', 'iw'
        ]
        additional_stopwords = ['münchen','zimmer', 'wohnung']
        my_stopwords_list.extend(additional_stopwords) # add some extra stop words

        #cloud = plot_wordcloud(clean_descriptions, my_stopwords_list)

    if VIZ['area_price']: #? Still dunno how to implement

        tosort_area_price = dataset[['Area','price']].copy()
        tosort_area_price.sort_values(by=['Area'], inplace=True)
        #tosort_area_price.plot(x ='Area', y='price', kind = 'line')
        plt.show()
        print(tosort_area_price.head(10))
        #plt.show()
        #ax = tosort_area_price['price'].plot()
        #tosort_area_price['price'].plot(ax=ax)
        #print(tosort_area_price.info())
