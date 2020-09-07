

# TODO
# + Averege area
# + Averege price
# + Most popular words in description
# + Pets allowed/no
# How long it stayed alive (until ads got disabled)
# Heatmap of prices/ locations to prove that city center is not more expensive
# Hearmap of offers - which district is the hootest and has more offers?
# Averege rooms ?? area??
# Area with most amount of immobilien offers
# + Destribution of new flat ADS per week
# + Destribution of new flat ads per day
# % of flats listed with full address
# 

from data_cleaning import int_float_price, clean_price, clean_online_since, conv_date_obj, int_float, get_weekday, get_online_hour, clean_description
from plotting import plot_bar_chart, plot_histogram, plot_cloud, plot_pie_chart
from db_handler import ini_tiny_db, dynamodb_connect, local_db_insert_data, scan_db
from tinydb import TinyDB, Query #TODO: redo later
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

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
weekday_ylabel = 'Averege number of ad posts'

# PRINT
#chart_week_dist = plot_bar_chart(weekday_objects, weekday_data,weekday_title, weekday_ylabel)

# Distribution of postings per day
hour_objects = []
for i in range(24):

    hour_objects.append(i)

hour_data = []

for hour_object in hour_objects:
    hour_data.append(sorted_hours[hour_object])


hour_title = 'Day posting distribution'
# PRINT
#chart_hour_dist = plot_histogram(online_hour_list,hour_title,24)
descriptions_list = []
for description_key in data:

    descriptions_list.append(description_key['description']) 

clean_description_text = clean_description(descriptions_list)  

# Generate word cloud
my_stopwords_list = ['mit','zi', 'im', 'voll', 'whg', 'und', 'von', 'der','die', 'nach', 'ab','uhr','um','zum', 'für','whg', 'eg', 'iw']
additional_stopwords = ['münchen','zimmer', 'wohnung']
my_stopwords_list.extend(additional_stopwords) # add some extra stop words
my_stopwords = set(STOPWORDS)
my_stopwords.update(my_stopwords_list)


# PRINT
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = my_stopwords).generate(clean_description_text)
cloud = plot_cloud(wordcloud)


pets_data_list = []

for pet_info in data:
    try:
        pets_data_list.append(pet_info['petsAllowed'])
    except TypeError:
        pass
    except KeyError:
        pass

pets_data_list = ['Not Specified' if x=='' else x for x in pets_data_list]

pets_labels = ['Nein', 'Ja','Not Specified', 'Nach Vereinbarung']
sorted_pets_data = Counter(pets_data_list)


pet_data_dist = []

for pet_data in pets_labels:

    pet_data_dist.append(sorted_pets_data[pet_data])

# PRINT
#chart_pie = plot_pie_chart(pet_data_dist, pets_labels)

def clean_address_data(address_str):
    
    address_str = address_str.lower()
    if 'anbieter' in address_str:
        return address_str.split(',')[0]
    else:
        return address_str

address_list = []

for address in data:

    clean_address = clean_address_data(address['address'])
    
    address_list.append(clean_address)

with open('clean_addresses.txt', 'w') as f:
    for item in address_list:
        f.write("%s\n" % item)