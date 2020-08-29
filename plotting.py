#

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt




def plot_bar_chart(objects, data, title, ylabel):

    
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, data, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)
    plt.title(title)

    return plt.show()


ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
def plot_histogram(data, title, n_bins = 12):

    plt.hist(data, n_bins, facecolor='green', alpha= 0.5, rwidth = 0.5)
    plt.xlim(0,24)
    plt.xticks(ticks)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=15)
    plt.ylabel('Avr Frequency',fontsize=15)
    plt.xlabel('Value',fontsize=15)
    plt.title(title)

    return plt.show()