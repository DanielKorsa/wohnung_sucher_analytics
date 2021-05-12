#
import pprint
from tinydb import TinyDB, Query
import boto3
from boto3.dynamodb.conditions import Key, Attr




def dynamodb_connect(db_name):
    '''
    Get AWS DynamoDB instance
    '''

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(db_name)

    return table

def scan_db(table_instance, attribute, search_criteria):
    '''
    Scan database and get results based on attribute and search criteria
    '''
    response = table_instance.scan(
        FilterExpression=Key(attribute).eq(search_criteria)
        #attr = 'source', search_criteria = 'immoscout24'
    )

    return response['Items']


def ini_tiny_db(db_name):
    '''
    Initialize tiny db
    '''
    local_db_name = TinyDB(db_name)
    local_db_instance = local_db_name.table('wohnung_sucher_analytics_table')

    return local_db_instance


def local_db_insert_data(dynamo_db_content, local_db):

    for db_data in dynamo_db_content:

        local_db.insert(db_data)
