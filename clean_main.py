#
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
from db_handler import dynamodb_connect, scan_db
from data_cleaning import clean_price, clean_online_since_date, clean_online_since_time, clean_description, clean_address_data
from plotting_data_prep import weekly_freq_prep, daily_freq_prep, pet_info_prep
from plotting import plot_bar_chart, plot_histogram, plot_pie_chart, plot_wordcloud
from new_google_maps_handler import geocode_address, read_ini_file, g_maps_auth, unpack_geocoded_data

CONF_FILE = 'config.ini'

UPDATE_DB = False
CLEAN_DATA = False
GOOGLE_GEOCODE = False
PRINT = True
TO_PRINT = ['text_info']

#! UPDATING DB
if UPDATE_DB:
    '''
    Update dataset from AWS DynamoDB
    '''
    db_instance = dynamodb_connect('wohnung_sucher_db')
    db_full_content = scan_db(db_instance,'source', 'immoscout24')
    dataset = pd.DataFrame(db_full_content)
    #dataset.to_csv('PANDAS_CSV.csv', sep='\t', encoding='utf-8', index=False)

else:
    '''
    Get local CLEAN copy of dataset
    '''
    dataset = pd.read_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8')


#! CLEANING DATA
#TODO mb put it to data_cleaning.py ???
if CLEAN_DATA:

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

    #geo_dataset = [dataset.price > 1290] #! TESTING 
    #print(geo_dataset.info()) #? SLICE DATASET
    api_key = read_ini_file(CONF_FILE, 'TOKENS', 'GMAPIKEY')
    gmaps_ref = g_maps_auth(api_key)
    city_dist_list = []
    lat_list = []
    lang_list = []

    addresses = dataset['formattedAddress'].tolist()
    for address in addresses:
        print(address)
        geocoded_data = geocode_address(gmaps_ref, address)
        city_dist, lat, lang = unpack_geocoded_data(geocoded_data)
        city_dist_list.append(city_dist)
        lat_list.append(lat)
        lang_list.append(lang)



    dataset['cityDistrict'] = city_dist_list
    dataset['lat'] = lat_list
    dataset['lang'] = lang_list

    #! write clean data to csv
    dataset.to_csv('PANDAS_GEOCODED.csv', sep='\t', encoding='utf-8', index=False)

#! PRINTING & PLOTTING
if PRINT:

    if 'text_info' in TO_PRINT:

        avr_area = dataset['Area'].mean()
        print('Averege area of a 2 room apartment in Munich is {} sq m'.format("%.2f" % avr_area))

        avr_price = dataset['price'].mean()
        print('Averege price of a 2 room apartment in Munich is {} euro'.format("%.2f" % avr_price))

        no_address = dataset['formattedAddress'].apply(lambda only_post: only_post.split(' ')[0].isdigit())
        falses, trues = no_address.value_counts().to_list() # trues = full address is not provided
        no_address_perc = (trues / (falses + trues)) * 100
        print('Only {} percent of ads reveal the real address'.format("%.1f" % no_address_perc))


    if 'price_hist' in TO_PRINT:

        dataset['price'].plot(kind='density')
        plt.show()

    if 'weekly_dist' in TO_PRINT:
        weekday_title = 'Weekly new flat posting distribution'
        weekday_ylabel = 'Averege number of ad posts'
        weekday_data, weekday_objects = weekly_freq_prep(dataset['onlineSinceDate'])
        chart_week_dist = plot_bar_chart(weekday_objects, weekday_data, title=weekday_title, ylabel=weekday_ylabel)

    if 'daily_dist' in TO_PRINT:

        hour_title = 'Day posting distribution'
        hourly_freq = daily_freq_prep(dataset['onlineSinceTime'])
        chart_hour_dist = plot_histogram(data=hourly_freq,title=hour_title, n_bins=24)

    if 'pet_data' in TO_PRINT:

        pet_data_dist, pets_labels = pet_info_prep(dataset['petsAllowed'])
        print(pets_labels)
        chart_pie = plot_pie_chart(pet_data_dist, pets_labels)

    if 'wordcloud' in TO_PRINT:

        clean_descriptions = clean_description(dataset['description'])

        # Generate word cloud
        my_stopwords_list = [
            'mit', 'zi', 'im', 'voll', 'whg', 'und', 'von', 'der', 'die',
            'nach', 'ab', 'uhr', 'um', 'zum', 'für', 'whg', 'eg', 'iw'
        ]
        additional_stopwords = ['münchen','zimmer', 'wohnung']
        my_stopwords_list.extend(additional_stopwords) # add some extra stop words

        cloud = plot_wordcloud(clean_descriptions, my_stopwords_list)

    if 'area_price' in TO_PRINT: #? Still dunno how to implement

        tosort_area_price = dataset[['Area','price']].copy()
        tosort_area_price.sort_values(by=['Area'], inplace=True)
        #tosort_area_price.plot(x ='Area', y='price', kind = 'line')
        plt.show()
        print(tosort_area_price.head(10))
        #plt.show()
        #ax = tosort_area_price['price'].plot()
        #tosort_area_price['price'].plot(ax=ax)
        #print(tosort_area_price.info())




#! Pandas info prints
#print(list(dataset)) # Get headers
# print(dataset.head(3)) # Get first N dataframe values
# print(dataset.info()) # Get dataset info
# print(dataset.dtypes)
