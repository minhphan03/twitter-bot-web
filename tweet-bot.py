from threading import Thread
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

#open the list of the words

def tweeter():
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


def retweeter():
    while True:
        data = api.user_timeline(screen_name='MerriamWebster', count=7)
        for tweet in data:
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)
        sleep(28800)

        data2 = api.user_timeline(screen_name='Dictionarycom', count=7)

        for tweet in data2:
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)

        sleep(28800)

        data3 = api.user_timeline(screen_name='Thesauruscom', count=7)

        for tweet in data3:
            try:
                if "#SynonymOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break

            except tweepy.TweepError as e:
                print(e)
        sleep(28800)

if __name__ == "__main__":
    Thread(target=retweeter()).start()
    Thread(target=tweeter()).start()

