#
from datetime import date, datetime
import calendar
import re
import random

def clean_description(descr_list):
    """[Clean description text for printing a word cloud graph]

    Args:
        descr_list ([list]): [list of descriptions]

    Returns:
        [str]: [clean str]
    """
    plain_text = ' '.join(descr_list)
    pure_text = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿ/]+', ' ', plain_text)
    words_list = pure_text.split(' ')
    clean_words_list = [word.lower() for word in words_list]
    clean_text = ' '.join(clean_words_list)

    return clean_text

def clean_online_since_date(date_time_str):
    """[Clean and replace Online Since Date if no data]

    Args:
        date_time_str ([str]): [Format: '2020-08-27T09:30:18']

    Returns:
        [str]: [Format 2020-08-'01]
    """
    if date_time_str == 'no data':
        online_date = '2020-08-' + str(random.randint(16,21))
    else:
        online_date = date_time_str.split('T')[0]

    return online_date

def clean_online_since_time(date_time_str):
    """[Clean and replace Online Since Time if no data]

    Args:
        date_time_str ([str]): [Format: '2020-08-27T09:30:18']

    Returns:
        [str]: [Format '21:30:18']
    """
    if date_time_str == 'no data':
        online_time = str(random.randint(0,24)) + ':30:18'
    else:
        online_time = date_time_str.split('T')[1]

    return online_time

def conv_datestr_to_weekday(date_str):
    """[Converts "2020-08-17" str into weekday "Monday" str]

    Args:
        date_str ([str]): [Format: "2020-08-17"]

    Returns:
        [str]: [Format: Monday]
    """
    format_str = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, format_str)
    weekday = calendar.day_name[date_obj.weekday()]

    return weekday

def clean_price(price):
    """[Prices on web site have different separator, this func is cleaning it]

    Args:
        price ([str]): [price with . or , or no separator]

    Returns:
        [int]: [Price int]
    """
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
    """[Make adresses scraped from the website uniform]

    Args:
        address_str ([str]): [address with different formatting]

    Returns:
        [str]: [clean address in lowercase]
    """
    address_str = address_str.lower()
    if 'anbieter' in address_str:
        return address_str.split(',')[0]
    else:
        return address_str

def weekly_freq_prep(data_column):
    """[Prepare data for weekly freq plot]

    Args:
        data_column ([]): [description]

    Returns:
        [type]: [description]
    """
    weekdays_freq = data_column.apply(conv_datestr_to_weekday).value_counts().to_dict() # Get freq of elements and to dict
    weekday_objects = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] # to arrange in right order
    weekday_data = [weekdays_freq[weekday_object] for weekday_object in weekday_objects]

    return weekday_data, weekday_objects

def daily_freq_prep(data_column):
    """[Prepare data for daily freq plot]

    Args:
        data_column ([type]): [description]

    Returns:
        [type]: [description]
    """
    hourly_freq = data_column.apply(lambda hour: int(hour.split(':')[0])).tolist() # Get hours and tolist

    return hourly_freq

def pet_info_prep(data_column):
    """[Prepare data for pie chart]

    Args:
        data_column ([type]): [description]

    Returns:
        [type]: [description]
    """
    pets_labels = ['Nein', 'Ja','Not Specified', 'Nach Vereinbarung']
    sorted_pets_data = data_column.value_counts().to_dict()
    pet_data_dist = [sorted_pets_data[pet_data] for pet_data in pets_labels]

    return pet_data_dist, pets_labels

