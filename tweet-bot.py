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
        for tweet in api.user_timeline(screen_name='MerriamWebster', count=6):
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)


        for tweet in api.user_timeline(screen_name='Dictionarycom', count=5):
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)

        for tweet in api.user_timeline(screen_name='Thesauruscom', count=5):
            try:
                if "#SynonymOfTheDay" in tweet.text:
                    print(tweet.text)
                    tweet.retweet()
                    break

            except tweepy.TweepError as e:
                print(e)

        print("time until next retweet session: 20000s")
        await asyncio.sleep(20000)




async def main():
    task1 = asyncio.create_task(tweeter())
    task2 = asyncio.create_task(retweeter())
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
