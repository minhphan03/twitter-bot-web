import asyncio
import tweepy
import random
from os import environ

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
                #api.update_status(line)

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
                    #tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)
        await asyncio(28800)

        data2 = api.user_timeline(screen_name='Dictionarycom', count=5)

        for tweet in data2:
            try:
                if "#WordOfTheDay" in tweet.text:
                    print(tweet.text)
                    #tweet.retweet()
                    break
            except tweepy.TweepError as e:
                print(e)

        await asyncio.sleep(28800)

        data3 = api.user_timeline(screen_name='Thesauruscom', count=5)

        for tweet in data3:
            try:
                if "#SynonymOfTheDay" in tweet.text:
                    print(tweet.text)
                    #tweet.retweet()
                    break

            except tweepy.TweepError as e:
                print(e)
        await asyncio.sleep(28800)

async def main():
    task1 = asyncio.create_task(tweeter())
    task2 = asyncio.create_task(retweeter())
    await task1
    await task2
if __name__ == "__main__":
    # event = threading.Event()
    # t2 = threading.Thread(target=retweeter())
    # t1 = threading.Thread(target=tweeter())
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()

    asyncio.run(main())
