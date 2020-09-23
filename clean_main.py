
import pprint
import pandas as pd

#
from db_handler import dynamodb_connect, scan_db

UPDATE_DB = False
CLEAN_DATA = True

#dataset = pd.read_json('wohnung_sucher_analytics_db.json')

#dataset.to_csv('PANDAS.csv', sep='\t', encoding='utf-8')

if UPDATE_DB:
    '''
    Update dataset from AWS DynamoDB
    '''
    db_instance = dynamodb_connect('wohnung_sucher_db')
    db_full_content = scan_db(db_instance,'source', 'immoscout24')
    dataset = pd.DataFrame(db_full_content)
    dataset.to_csv('PANDAS_CSV.csv', sep='\t', encoding='utf-8', index=False)
    
else:
    '''
    Get local copy of dataset
    '''
    dataset = pd.read_csv('PANDAS_CSV.csv', sep='\t', encoding='utf-8')
    
    
# Cleaning data, saving it as another CSV
#! Clean area, onlineSince, petsAllowed, Price
#! Try apply function of pandas
if CLEAN_DATA:
    
    columns_to_drop = ['email', 'phone', 'source'] # Remove columns which are not used
    dataset.drop(columns_to_drop, inplace=True, axis=1)
    


#employees['Age'].hist()

#print(list(dataset)) # Get headers
print(dataset.head(10)) # Get first N dataframe values
#print(dataset.info()) # Get dataset info