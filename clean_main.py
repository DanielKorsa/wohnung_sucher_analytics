#
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
from db_handler import dynamodb_connect, scan_db
from data_cleaning import clean_price, clean_online_since_date, clean_online_since_time
from plotting_data_prep import weekly_freq_prep, daily_freq_prep, pet_info_prep
from plotting import plot_bar_chart, plot_histogram, plot_pie_chart

UPDATE_DB = False
CLEAN_DATA = False
PRINT = True
TO_PRINT = ['']

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
#TODO remove duplicate based on price+address
#TODO mb put it to data_cleaning.py ???
if CLEAN_DATA:

    columns_to_drop = ['email', 'phone', 'source'] # Remove columns which are not used
    dataset.drop(columns_to_drop, inplace=True, axis=1)

    dataset['Area'] = dataset['Area'].apply(lambda area: float(area.split(' ')[0].replace(',','.'))) # clean Area data
    dataset['price'] = dataset['price'].apply(clean_price) # Clean price from . ,
    dataset['petsAllowed'] = dataset['petsAllowed'].fillna(value='Not Specified') # Fill PetsAllowed NaN with Nach Vereinbarung
    dataset['onlineSinceDate'] = dataset['onlineSince'].apply(clean_online_since_date)
    dataset['onlineSinceTime'] = dataset['onlineSince'].apply(clean_online_since_time)

    dataset.drop('onlineSince', inplace=True, axis=1) #TODO cheeck why index shifts 
    #! write clean data to csv
    dataset.to_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8', index=False) 

#! PRINTING
# area_hist = dataset['Area'].hist()
if PRINT:
    print('PRINTING') 
    # dataset['price'].plot(kind='density')
    # plt.show()
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

    #weekdays_freq.plot.bar(x="Weekday", y="N of ads", rot=70, title="Weekly ads distribution")
    #plt.show()
    #print(type(weekdays_freq))
    #weekly_dist_hist = dataset['weekdays'].plot.bar(x="Weekday", y="N of ads", rot=70, title="Weekly ads distribution")
    #plt.show()


#print(list(dataset)) # Get headers
#dataset.to_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8', index=False) #! write clean data to csv
# print(dataset.head(3)) # Get first N dataframe values
# print(dataset.info()) # Get dataset info
# print(dataset.dtypes)
