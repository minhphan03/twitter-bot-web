from concurrent.futures import ThreadPoolExecutor
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

def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


if __name__ == "__main__":
    run_io_tasks_in_parallel([
        retweeter(), tweeter(),
    ])