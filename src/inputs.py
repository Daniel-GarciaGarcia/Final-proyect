
import os
import json
from dotenv import load_dotenv
import requests_oauthlib
import tweepy
import pandas as pd
import time

api = tweepy.API(auth, wait_on_rate_limit=True)

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


