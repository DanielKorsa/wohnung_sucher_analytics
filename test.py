


import re

descriptions = ['Helle 2 Zi.-Wohnung mit super großer Wohnküche',
'Helle 2 Zi.-Wohnung mit super großer Wohnküche',
'Ansprechende 3-Zimmer-Wohnung mit Einbauküche und Balkon nähe Hirschgarten'
]



plain_text = ' '.join(descriptions)


pure_text = re.sub('[^A-Za-z0-9]+', ' ', plain_text)
words_list = pure_text.split(' ')
clean_words_list = [word.lower() for word in words_list]
clean_text = ' '.join(clean_words_list)
print(clean_words_list)


# Import packages
import matplotlib.pyplot as plt
#matplotlib inline
# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(10, 10))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")
    return plt.show()


# Import package
from wordcloud import WordCloud, STOPWORDS
# Generate word cloud
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(clean_text)
# Plot
cloud = plot_cloud(wordcloud)