from multiprocessing import Process
import tweepy
import random
from os import environ
from time import sleep

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


while True:
    with open('list.txt') as f:
        lines = [line.rstrip('\n') for line in f if line != '\n']

    shuffled_lines = random.sample(lines, len(lines))

    for line in shuffled_lines:
        try:
            print(line)
            api.update_status(line)

        except tweepy.TweepError as e:
            print(e.reason)
        sleep(21600)

