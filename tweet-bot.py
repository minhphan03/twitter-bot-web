import asyncio
import tweepy
import random
from os import environ
import datetime

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#open the list of the words

async def tweeter():
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
            await asyncio.sleep(21600)


async def retweeter():
    while True:
        data = api.user_timeline(screen_name='MerriamWebster', count=3)
        for tweet in data:
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session ", getTime())
                    await asyncio.sleep(28800)
                    break
            except tweepy.TweepError as e:
                print(e)



        data2 = api.user_timeline(screen_name='Dictionarycom', count=5)

        for tweet in data2:
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    print("time until next retweet session ", getTime())
                    await asyncio.sleep(28800)
                    break
            except tweepy.TweepError as e:
                print(e)

        data3 = api.user_timeline(screen_name='Thesauruscom', count=5)

        for tweet in data3:
            try:
                if "#SynonymOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break

            except tweepy.TweepError as e:
                print(e)
        print("time until next retweet session ", getTime())
        await asyncio.sleep(getTime())

def getTime():
    t1 = datetime.datetime.today()
    t2 = datetime.datetime(t1.year, t1.month,t1.day, 6,00,00)
    now = datetime.datetime.now()

    result = (t2-now).total_seconds()

    if result < 0:
        result += 24*3600
    return int(round(result))

async def main():
    task1 = asyncio.create_task(tweeter())
    task2 = asyncio.create_task(retweeter())
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
