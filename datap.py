# -*- coding: utf-8 -*-
"""vishalghadageAnalysisnlp.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OE58yuhWhw9K229-mB-5DaHNo7dvhP2x
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import nltk
import string
import spacy
# import all required library

df=pd.read_excel("/content/Assignment.xlsx")

df

df.shape

df.isnull().sum()

df.isnull().sum()

df['Article'].apply(len)
# checking length

df['Article'] = df['Article'].str.lower()
# convert lowercase

nltk.download('punkt')

nltk.download('stopwords')
# import

def remove_punctuation(text):
  for punctuation in string.punctuation:
    text = text.replace(punctuation, ' ')
  return text
df['Article'] = df['Article'].apply(remove_punctuation)
df
# remove punctuations

def preprocess_text(article):
    # Remove punctuation
    article = re.sub(r'[^\w\s]', '', article)

    # Tokenize the article into words
    words = word_tokenize(article)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Join the words back into a string
    cleaned_article = ' '.join(words)

    return cleaned_article

df['Article'] = df['Article'].apply(preprocess_text)

nlp = spacy.load("en_core_web_sm")
def lemmatize_text(article):
    doc = nlp(article)
    lemmatized_words = [token.lemma_ for token in doc]
    return ' '.join(lemmatized_words)
df['Article'] = df['Article'].apply(lemmatize_text)
# preprocessing

df

df['Article'].str.len()

def classify_mood(article):
    analysis = TextBlob(article)    #TextBlob is a part of the TextBlob library and provides a simple API for natural language processing tasks.
    sentiment = analysis.sentiment.polarity

    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

df1 = pd.DataFrame(df)
df1['Mood'] = df1['Article'].apply(classify_mood)
# using TextBlob library perform sentiment analysis

df1

!pip install matplotlib-venn

pip install vaderSentiment

df1

# df1

nlp = spacy.load("en_core_web_sm")

def extract_aspect_words(article_text):
    aspect_words = []
    doc = nlp(article_text)
    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:
            aspect_words.append(token.lemma_)
    return aspect_words

aspect_word_dict = {}

for index, row in df.iterrows():
    aspect_words = extract_aspect_words(row['Article'])
    for word in aspect_words:
        if word in aspect_word_dict:
            aspect_word_dict[word] += 1
        else:
            aspect_word_dict[word] = 1
print(aspect_word_dict)
# make dictinary of common words

aspect_word_freq = {}
for word, freq in aspect_word_dict.items():

    if isinstance(freq, int):
        aspect_word_freq[word] = freq

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(aspect_word_freq)

plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
# wordcloud for analysis

nlp = spacy.load("en_core_web_sm")
def calculate_most_common_word(article_text):
    doc = nlp(article_text)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_counts = Counter(words)
    most_common_word = word_counts.most_common(1)
    if most_common_word:
        return most_common_word[0][0]
    else:
        return None

df1['Most_Common_Word'] = df1['Article'].apply(calculate_most_common_word)
# new feature

df1

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
def calculate_sentiment(article_text):
    sentiment_score = analyzer.polarity_scores(article_text)
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

df1['Sentiment'] = df1['Article'].apply(calculate_sentiment)
# sentiment

df1

df1.to_excel('Analysis Project.xlsx', index=False)

