#
from datetime import date, datetime
import calendar
import re
import random

def clean_description(descr_list):
    '''
    Clean description text for printing a word cloud graph
    '''
    plain_text = ' '.join(descr_list)
    #pure_text = re.sub('[^A-Za-z0-9]+', ' ', plain_text) # old
    pure_text = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿ/]+', ' ', plain_text)
    words_list = pure_text.split(' ')
    clean_words_list = [word.lower() for word in words_list]
    clean_text = ' '.join(clean_words_list)

    return clean_text

def clean_online_since_date(date_time_str):
    '''
    Str from db online_since = '2020-08-27T09:30:18'
    '''
    if date_time_str == 'no data':
        online_date = '2020-08-' + str(random.randint(16,21)) #TODO: make random date from 16-23 Sep
    else:
        online_date = date_time_str.split('T')[0]

    return online_date

def clean_online_since_time(date_time_str):
    '''
    Str from db online_since = '2020-08-27T09:30:18'
    '''
    if date_time_str == 'no data':
        online_time = str(random.randint(0,24)) + ':30:18' #TODO: make random date from 00-24 Sep
    else:
        online_time = date_time_str.split('T')[1]

    return online_time

def clean_online_since(date_time_str):
    '''
    Str from db online_since = '2020-08-27T09:30:18'
    '''
    online_date = date_time_str.split('T')[0]
    online_time = date_time_str.split('T')[1]
    
    return online_date, online_time

def conv_date_obj(date_str):
    '''
    make date obj out of str
    '''
    format_str = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, format_str)

    return date_obj

def get_online_hour(time_str):
    
    return int(time_str.split(':')[0])

def get_weekday(date_obj):
    '''
    '''
    weekday = calendar.day_name[date_obj.weekday()]

    return weekday

def conv_datestr_to_weekday(date_str):
    '''
    Converts "2020-08-17" str into weekday "Monday" str
    '''
    format_str = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, format_str)
    weekday = calendar.day_name[date_obj.weekday()]

    return weekday

def int_float(str_num):
    '''
    convert str to float
    '''
    try:
        return int(str_num)
    except ValueError:
        return float(str_num.replace(',','.'))

def int_float_price(str_num):
    '''
    Convert price
    '''
    try:
        return int(str_num)
    except ValueError:
        return float(str_num.replace('.',','))

def clean_price(price):
    '''
    Prices on web site have different separator, this func is cleaning it
    '''
    price = price.split(' ')[0]

    if '.' in price:

        clean_price = price.replace('.', '')

        if ',' in clean_price:
            result = (int(clean_price.split(',')[0]))

        else:
            result = (int(clean_price))

    elif ',' in price:
            result = (int(price.split(',')[0]))

    else:
        result = (int(price))


    return result


def clean_address_data(address_str):

    address_str = address_str.lower()
    if 'anbieter' in address_str:
        return address_str.split(',')[0]
    else:
        return address_str

