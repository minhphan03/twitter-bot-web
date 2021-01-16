import tweepy
import random
import os
from os import environ
from time import sleep

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#open-file

with open('list.txt') as f:
    lines = [line.rstrip('\n') for line in f]

shuffled_lines = random.sample(lines, len(lines))

for line in shuffled_lines:
    try:
        print(line)
        api.update_status(line)

    except tweepy.TweepError as e:
        print(e.reason)
    sleep(900)