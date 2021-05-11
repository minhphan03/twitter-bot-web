import asyncio
import tweepy
import random
import requests
import re
from bs4 import BeautifulSoup
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
        with open('list.txt', "r") as f:
            lines = [line.rstrip('\n') for line in f if line != '\n']

        shuffled_lines = random.sample(lines, len(lines))

        for shuffledline in shuffled_lines:
            try:
                api.update_status(shuffledline)
                lines.remove(shuffledline)
                with open('list.txt', "w") as f:
                    for line in lines:
                            f.write(line + "\n")

            except tweepy.TweepError as e:
                print(e.reason)
            await asyncio.sleep(21600)


# because heroku restarts daily, no need to create a for loop to refresh page

async def retweeter():

    for tweet in api.user_timeline(screen_name='MerriamWebster', count=6):
        try:
            if "#WordOfTheDay" in tweet.text:
                print(tweet.text)
                tweet.retweet()
                print("time until next retweet session: 10000s")
                await asyncio.sleep(10000)

                break
        except tweepy.TweepError as e:
            print(e)


    for tweet in api.user_timeline(screen_name='Dictionarycom', count=5):
        try:
            if "#WordOfTheDay" in tweet.text:
                print(tweet.text)
                tweet.retweet()
                print("time until next retweet session: 10000s")
                await asyncio.sleep(10000)
                break
        except tweepy.TweepError as e:
            print(e)

    for tweet in api.user_timeline(screen_name='Thesauruscom', count=5):
        try:
            if "#SynonymOfTheDay" in tweet.text:
                print(tweet.text)
                tweet.retweet()
                print("time until next retweet session: 10000s")
                await asyncio.sleep(10000)
                break

        except tweepy.TweepError as e:
            print(e)

    for tweet in api.user_timeline(screen_name='OED', count=2):
        try:
            if "Word of the Day" in tweet.text:
                print(tweet.text)
                tweet.retweet()
                print("time until next retweet session: 10000s")
                await asyncio.sleep(10000)
                break

        except tweepy.TweepError as e:
            print(e)

async def reply_bot():
    print("retrieving mentions")
    for tweet in tweepy.Cursor(api.mentions_timeline).items(limit=1):

        with open("tweet_id.txt", "r") as f:
            tweet_id = f.read()
            print("the id is '" + tweet_id + "'")

        if str(tweet_id) == str(tweet.id):
            print("break.......")
            break
        else:
            print("enter else statement")
            with open("tweet_id.txt", "w") as f:
                f.write(str(tweet.id))
            print("the tweet id is" + str(tweet.id))
        if tweet.in_reply_to_status_id is not None:
            continue
        try:
            text = re.search(r'\s*(?<=(@thevocabbot)).*', tweet.text)
            result = webscraping(text.group().strip().split())
            api.update_status(status=f"@{tweet.user.screen_name} {result}", in_reply_to_status_id = tweet.id)
            print("sleep")
            await asyncio.sleep(200)
        except tweepy.TweepError as e:
            print(e)

def webscraping(word):
    try:
        link = "https://www.merriam-webster.com/dictionary/" + "+".join(word)
        r = requests.get(link)
        c = r.content

        soup = BeautifulSoup(c, 'html.parser')
        allcontent = soup.find('div', attrs={'class': 'vg'})

        content = allcontent.findAll('span', attrs={'class': 'dtText'})
        if len(content) > 3:
            content = content[:3]
        strings = []

        for i in content:
            text = re.search(":\s.*", i.get_text()).group().strip()[2:]
            if re.search(r"sense \w+", i.get_text()) is not None:
                print(re.search(r"sense \w+", i.get_text()).group())
                text = re.sub(re.search(r"sense \w+", i.get_text()).group(), "", text)
            strings.append(text)

        return " ".join(word) + ": " + "; ".join(strings) + ". See more at " + link

    except requests.exceptions:
        return "This word does not exist in Merriam Webster. Please look up manually or check your grammar. DM us if you have any request."


async def main():
    task1 = asyncio.create_task(tweeter())
    task2 = asyncio.create_task(retweeter())
    task3 = asyncio.create_task(reply_bot())
    await task1
    await task2
    await task3

if __name__ == "__main__":
    asyncio.run(main())
