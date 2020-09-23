
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
from db_handler import dynamodb_connect, scan_db
from data_cleaning import clean_price, clean_online_since_date, clean_online_since_time

UPDATE_DB = False
CLEAN_DATA = True
PRINT = False


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
    Get local copy of dataset
    '''
    dataset = pd.read_csv('PANDAS_CSV.csv', sep='\t', encoding='utf-8')


#! CLEANING DATA
#TODO remove duplicate based on price+address
#TODO mb put it to data_cleaning.py ???
if CLEAN_DATA:

    columns_to_drop = ['email', 'phone', 'source'] # Remove columns which are not used
    dataset.drop(columns_to_drop, inplace=True, axis=1)

    dataset['Area'] = dataset['Area'].apply(lambda area: float(area.split(' ')[0].replace(',','.'))) # clean Area data
    dataset['price'] = dataset['price'].apply(clean_price) # Clean price from . ,
    dataset['petsAllowed'] = dataset['petsAllowed'].fillna(value='Nach Vereinbarung') # Fill PetsAllowed NaN with Nach Vereinbarung
    dataset['onlineSinceDate'] = dataset['onlineSince'].apply(clean_online_since_date)
    dataset['onlineSinceTime'] = dataset['onlineSince'].apply(clean_online_since_time)

    dataset.drop('onlineSince', inplace=True, axis=1) #TODO cheeck why index shifts 
    #! write clean data to csv
    dataset.to_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8', index=False) 

#! PRINTING
# area_hist = dataset['Area'].hist()
if PRINT:
    print(dataset['price'].dtypes) # print data type of a column
    dataset['price'].plot(kind='density')
    plt.show()

#print(list(dataset)) # Get headers
#dataset.to_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8', index=False) #! write clean data to csv
print(dataset.head(3)) # Get first N dataframe values
print(dataset.info()) # Get dataset info