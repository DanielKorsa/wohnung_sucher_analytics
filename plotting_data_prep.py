#
from data_cleaning import conv_datestr_to_weekday

def weekly_freq_prep(data_column):
    '''
    '''
    weekdays_freq = data_column.apply(conv_datestr_to_weekday).value_counts().to_dict() # Get freq of elements and to dict
    #print(weekdays_freq)
    weekday_objects = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] # to arrange in right order
    weekday_data = []
    for weekday_object in weekday_objects:
        weekday_data.append(weekdays_freq[weekday_object])
    print(weekday_data)

    return weekday_data, weekday_objects