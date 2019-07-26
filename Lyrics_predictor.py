'''
CBGB-Lyrics-Checker
'''

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix

import seaborn as sns
import matplotlib.pyplot as plt


ARTIST = ['Blondie', 'Iggy Pop', 'Ramones', 'Talking Heads']
ARTIST_LAST = ['Blondie', 'Pop', 'Ramones', 'Heads']

def create_train_test_df(df):

    df_test = pd.DataFrame(columns=['text', 'label'])
    df_train = pd.DataFrame(columns=['text', 'label'])

    artist_count = {'Ramones': 0, 'Heads': 0, 'Blondie': 0, 'Pop': 0}
    count_max = 150

    for i, j in df.iterrows():
        if str(j).split()[-5] in ARTIST_LAST:
            if artist_count[str(j).split()[-5]] < count_max:
                df_train.loc[i] = [df['text'][i]] + [df['label'][i]]
                artist_count[str(j).split()[-5]] += 1
            else:
                df_test.loc[i] = [df['text'][i]] + [df['label'][i]]
        else:
            continue

    return df_train, df_test


def vectorize(df_train):
    cv = CountVectorizer(stop_words='english')
    tf = TfidfTransformer()

    vec_train = cv.fit_transform(df_train['text'].values.tolist())
    vec2_train = tf.fit_transform(vec_train)

    return cv, tf, vec2_train


def fit_model(vec2_train, df_train):
    X = vec2_train
    y = df_train['label']
    m = MultinomialNB()
    m.fit(X, y)

    return m


def prediction(df_test, cv, tf, m):
    vec_test = cv.transform(df_test['text'].values.tolist())
    vec2_test = tf.transform(vec_test)

    ypred = m.predict(vec2_test)
    df_test['ypred'] = ypred

    return df_test


def plot_heatmap(df_test):
    plt.figure(figsize=(5, 5))
    sns.heatmap(confusion_matrix(df_test['label'], df_test['ypred']),
                annot=True,
                cmap='Oranges',
                xticklabels=ARTIST,
                yticklabels=ARTIST
                )
    plt.show()

#--------------------------------------------

def main():
    df = pd.read_csv('output_lyrics.csv')
    df_train, df_test = create_train_test_df(df)
    cv, tf, vec2_train = vectorize(df_train)
    m = fit_model(vec2_train, df_train)
    df_test = prediction(df_test, cv, tf, m)
    plot_heatmap(df_test)

main()
