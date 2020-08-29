

# TODO
# + Averege area
# + Averege price
# Most popular words in description
# Pets allowed/no
# How long it stayed alive (until ads got disabled)
# Heatmap of prices/ locations to prove that city center is not more expensive
# Averege rooms ?? area??
# Area with most amount of immobilien offers
# Destribution of new flats per week
#Destribution of new flat ads per day



from data_cleaning import int_float_price, clean_price, clean_online_since, conv_date_obj, int_float, get_weekday, get_online_hour
from plotting import plot_bar_chart, plot_histogram
from db_handler import ini_tiny_db, dynamodb_connect, local_db_insert_data, scan_db
from tinydb import TinyDB, Query #TODO: redo later
from collections import Counter


UPDATEDBFROMAWS = False

local_db = ini_tiny_db('wohnung_sucher_analytics_db.json')


if UPDATEDBFROMAWS:
    db_instance = dynamodb_connect('wohnung_sucher_db')
    db_full_content = scan_db(db_instance,'source', 'immoscout24')
    local_db_insert_data(db_full_content, local_db)
    #pprint.pprint(db_full_content)

flat = Query()
data = local_db.search(flat['source'] == 'immoscout24')


# Get averege flat area
areas_data = []
for area in data:
    areas_data.append(int_float(area['Area'].split(' ')[0]))

avrg_area = sum(areas_data) / len(areas_data)
print('Averege area of a 2 room apartment in Munich is {} sq m'.format("%.2f" % avrg_area))


# Get averege flat prices
prices_data = []
for price in data:
    prices_data.append(clean_price(price['price'].split(' ')[0]))

avrg_price = sum(prices_data) / len(prices_data)
print('Averege price of a 2 room apartment in Munich is {} euro'.format("%.2f" % avrg_price))




# Distribution of new flats per week
online_since_list = []
online_hour_list = []

for online_since in data:

    my_date, my_time = clean_online_since(online_since['onlineSince'])
    date_obj = conv_date_obj(my_date)
    weekday = get_weekday(date_obj)
    online_since_list.append(weekday)
    online_hour_list.append(get_online_hour(my_time))
    
sorted_weekdays = Counter(online_since_list)
sorted_hours = Counter(online_hour_list)

#print(sorted_hours)

weekday_objects = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_data = []
for weekday_object in weekday_objects:
    weekday_data.append(sorted_weekdays[weekday_object])

weekday_title = 'Weekly new flat posting distribution'
weekday_ylabel = 'times'

#chart_week_dist = plot_bar_chart(weekday_objects, weekday_data,weekday_title, weekday_ylabel)

# Distribution of postings per day
hour_objects = []
for i in range(24):

    hour_objects.append(i)

hour_data = []

for hour_object in hour_objects:
    hour_data.append(sorted_hours[hour_object])


hour_title = 'Day posting distribution'
chart_hour_dist = plot_histogram(online_hour_list,hour_title,24)
#hour_objets = sorted(list(sorted_hours.keys()))

print(hour_objects)
print(hour_data)