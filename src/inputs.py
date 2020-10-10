
import os
import json
from dotenv import load_dotenv
import requests_oauthlib
import tweepy
import pandas as pd
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def get_auth():

    load_dotenv()
    CONSUMER_KEY=os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET=os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET=os.getenv("ACCESS_SECRET")
    my_auth=requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    return my_auth



tweets = []


def query_to_csv(text_query, count):
    try:
        tweets = tweepy.Cursor(api.search, q=text_query).items(count)
        tweets_list = [[tweet.id, tweet.created_at, tweet.text] for tweet in tweets]

        # tweet information
        tweets_df = pd.DataFrame(tweets_list, columns=['ID', 'Datetime', 'Text'])

        tweets_df.to_csv('{}-tweets.csv'.format(text_query), sep=',', index=False)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

def process_tweets(tweet):
    
    # Remove links
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    
    # Remove mentions and hashtag
    tweet = re.sub(r'\@\w+|\#','', tweet)
    
    # Tokenize the words
    tokenized = word_tokenize(tweet)

    # Remove the stop words
    tokenized = [token for token in tokenized if token not in stopwords.words("english")] 

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokenized = [lemmatizer.lemmatize(token, pos='a') for token in tokenized]

    # Remove non-alphabetic characters and keep the words contains three or more letters
    tokenized = [token for token in tokenized if token.isalpha() and len(token)>2]
    # Fit and transform the vectorizer
    return tokenized
    
