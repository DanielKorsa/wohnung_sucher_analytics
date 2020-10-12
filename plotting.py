#

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

FONT = {'fontname':'Arial'}
TITLE_S = 27
LABEL_S = 23
def plot_hist_pd(data, title, ylbl, xlbl):

    data.plot(kind='density')
    #weight = 'bold'
    plt.ylabel(ylbl, fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.xlabel(xlbl, fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.title(title ,fontsize=TITLE_S, pad=30, style='italic', **FONT)
    plt.xticks(fontsize=16)
    plt.tick_params(axis='x', which='major', pad=10)

    plt.yticks(fontsize=5)
    #plt.ylim([0,0.025])
    plt.xlim([300,1700])
    return plt.show()

def plot_bar_chart(objects, data, title='', ylabel='', bar_color = 'deepskyblue'):


    y_pos = np.arange(len(objects))
    #plt.box(on=None)
    plt.bar(y_pos, data, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=LABEL_S, rotation='vertical', **FONT)
    plt.ylabel(ylabel, fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.title(title, fontsize=TITLE_S, pad=30, style='italic', **FONT)
    #plt.ylim([0,1300])
    plt.bar(range(len(data)), data, color=bar_color)

    return plt.show()

def plot_bar_chart_dists(objects, data, title='', ylabel='', bar_color = 'deepskyblue'):


    y_pos = np.arange(len(objects))
    #plt.box(on=None)
    plt.bar(y_pos, data, align='center', alpha=0.5)
    plt.yticks(fontsize=19, **FONT)
    plt.xticks(y_pos, objects, fontsize=19,rotation='vertical',  **FONT)
    plt.ylabel(ylabel, fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.title(title, fontsize=TITLE_S, pad=30, style='italic', **FONT)
    #plt.ylim([0,1300])
    plt.bar(range(len(data)), data, color=bar_color)

    return plt.show()

ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
def plot_histogram(data, title, n_bins = 12):

    plt.hist(data, n_bins, facecolor='limegreen', alpha= 0.5, rwidth = 0.5)
    plt.xlim(0,24)
    plt.xticks(ticks)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylabel('Number of apartment listings',fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.xlabel('Hour',fontsize=LABEL_S, labelpad=20, weight = 'bold', **FONT)
    plt.title(title, fontsize=TITLE_S, pad=30, style='italic', **FONT)
    plt.tick_params(axis='x', which='major', pad=10)
    plt.tick_params(axis='y', which='major', pad=10)

    return plt.show()


def plot_wordcloud(cloud_words, extra_stopwords):

    new_stopwords = set(STOPWORDS)
    new_stopwords.update(extra_stopwords)

    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='white', colormap='plasma', collocations=False, stopwords = new_stopwords).generate(cloud_words)
    # Set figure size
    plt.figure(figsize=(10, 10))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")

    return plt.show()



def plot_pie_chart(pets_data, objects):


    colors = ['tomato', 'lightgrey', 'gold', 'yellowgreen']
    explode = (0, 0, 0, 0.1)  # explode 1st slice
    plt.pie(x = pets_data, explode = explode, shadow = True, colors = colors, labels = objects, startangle =180, autopct='%.1f%%',textprops={'fontsize': 18})
    plt.title('Pet friendly apartments', fontsize=TITLE_S, pad=30, style='italic', **FONT)
    plt.axis('equal')


    return plt.show()


