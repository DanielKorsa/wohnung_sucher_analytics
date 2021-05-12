#

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
#from wordcloud import WordCloud, STOPWORDS




def plot_bar_chart(objects, data, title='', ylabel='', bar_color = 'blue'):


    y_pos = np.arange(len(objects))

    plt.bar(y_pos, data, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=12)
    plt.ylim([0,1300])
    plt.bar(range(len(data)), data, color=bar_color)

    return plt.show()


ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
def plot_histogram(data, title, n_bins = 12):

    plt.hist(data, n_bins, facecolor='green', alpha= 0.5, rwidth = 0.5)
    plt.xlim(0,24)
    plt.xticks(ticks)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel('Number of apartment listings',fontsize=15)
    plt.xlabel('Hour',fontsize=15)
    plt.title(title)

    return plt.show()


# def plot_wordcloud(cloud_words, extra_stopwords):

#     new_stopwords = set(STOPWORDS)
#     new_stopwords.update(extra_stopwords)

#     wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='white', colormap='plasma', collocations=False, stopwords = new_stopwords).generate(cloud_words)
#     # Set figure size
#     plt.figure(figsize=(10, 10))
#     # Display image
#     plt.imshow(wordcloud)
#     # No axis details
#     plt.axis("off")

#     return plt.show()



def plot_pie_chart(pets_data, objects):


    colors = ['lightcoral', 'yellowgreen', 'lightskyblue', 'gold']
    explode = (0, 0.1, 0, 0)  # explode 1st slice
    plt.pie(x = pets_data, explode = explode, shadow = True, colors = colors, labels = objects, startangle =180, autopct='%.1f%%')
    plt.title('Pet friendly apartments')
    plt.axis('equal')

    return plt.show()


