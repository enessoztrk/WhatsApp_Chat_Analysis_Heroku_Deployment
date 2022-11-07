import pandas as pd
import re
from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import emoji
import streamlit as st

stopwords = STOPWORDS

def get_msg_stats(df):

    # 1. users list
    n_users = sorted(df['user'].unique().tolist())

    # 2. count words
    words = []
    for msg in df['message']:
        ms = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', msg)
        for i in ms:
            if i != '' and i != 'media' and i != 'omitted':
                if i not in stopwords:
                    words.append(i)

    # 3. count media file
    count = 0
    for msg in df['message']:
        if msg == ' <media omitted>':
            count += 1

    # 4. extract url
    extract = URLExtract()  # object of urlextract, this will extract url from the msgs
    links = []
    for i in df['message']:
        links.extend(extract.find_urls(i))

    return len(n_users), df.shape[0], len(words), count, len(links)


def wordMap_without_stopwords(df):
    df['message'] = df['message'].apply(lambda x: x.lower())
    f = open('turkish', 'r')
    stopwords = f.read()
    words = []  # of entire words in msg columns
    for msg in df['message']:
        # split the message in words using regex
        ms = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?\s]', msg)
        for i in ms:
            if i != '' and i != 'media' and i != 'omitted':
                if i not in stopwords:
                    if i.isalnum():
                        words.append(i)

    # counts the frequency of each words
    word_count = dict(Counter(words))
    # creating df of word_count
    word_df = pd.DataFrame(list(word_count.items()), columns=['words', 'count'])
    # creating wordmap of word_count dict
    wc = WordCloud(width=1200, height=500, min_font_size=10, background_color='white', regexp=r"\w[\w']+")
    word_img = wc.generate_from_frequencies(word_count)
    return word_img,word_df


def wordMap_with_stopwords(df):
    df['message'] = df['message'].apply(lambda x: x.lower())
    words = []  # of entire words in msg columns
    for msg in df['message']:
        # split the message in words using regex
        ms = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?\s]', msg)
        for i in ms:
            if i != '' and i != 'media' and i != 'omitted':
                if i.isalnum():
                    words.append(i)

    # counts the frequency of each words
    word_count = dict(Counter(words))
    # creating df of word_count
    word_df = pd.DataFrame(list(word_count.items()), columns=['words', 'count'])
    # creating wordmap of word_count dict
    wc = WordCloud(width=1200, height=500, min_font_size=10, background_color='white', regexp=r"\w[\w']+")
    word_img = wc.generate_from_frequencies(word_count)
    return word_img,word_df


def get_emojis(df):
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['emoji','counts'])

    return emojis_df

# member who started and ended the chat in every day
def chat_start_end_by(data):
    date = data.groupby(by='date')
    chat_started_by = date.first()['user'].value_counts().reset_index()
    chat_started_by.columns = ['Member', 'Count']

    chat_ended_by = date.last()['user'].value_counts().reset_index()
    chat_ended_by.columns = ['Member', 'Count']

    return chat_started_by, chat_ended_by


def crosstab_dayNmonth(day,month):
    s = pd.crosstab(day, month)
    m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']
    month = s.columns.tolist()
    month_name = []
    for i in m:
        if i in month: month_name.append(i)
    return s[month_name]

# get url links
def get_liks(df):
    extract = URLExtract()  # object of urlextract, this will extract url from the msgs
    links = []
    for i in df['message']:
        links.extend(extract.find_urls(i))
    return pd.DataFrame({'Links':links})