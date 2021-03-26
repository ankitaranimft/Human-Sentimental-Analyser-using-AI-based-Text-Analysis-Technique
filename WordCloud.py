from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt #to display our wordcloud

import numpy as np #to get the color of our image
import webbrowser



#Content-related
text = open('Positive.txt', 'r').read()
stopwords = set(STOPWORDS)

#Appearance-related
wc2 = WordCloud(background_color = 'pink',
               stopwords = stopwords,height=400,width=400,
               )

wc2.generate(text)
wc2.to_file('Poscloud.png')


#Content-related
text = open('Negative.txt', 'r').read()
stopwords = set(STOPWORDS)

#Appearance-related
wc1 = WordCloud(background_color = 'white',
               stopwords = stopwords,height=400,width=400,
               )
wc1.generate(text)
wc1.generate(text)
wc1.to_file('Negcloud.png')


#Content-related
text = open('Neutral.txt', 'r').read()
stopwords = set(STOPWORDS)

#Appearance-related
wc = WordCloud(background_color = 'black',
               stopwords = stopwords,height=400,width=400,
               )
wc.generate(text)
wc.to_file('Neucloud.png')



