#
from datetime import date, datetime
import calendar



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




