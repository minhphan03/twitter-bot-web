import asyncio
import tweepy
import random
import requests
import re
import datetime
from bs4 import BeautifulSoup
from os import environ

# CONSUMER_KEY = environ['CONSUMER_KEY']
# CONSUMER_SECRET = environ['CONSUMER_SECRET']
# ACCESS_TOKEN = environ['ACCESS_TOKEN']
# ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# open the list of the words

def webscraping(word)->str:
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

        return "; ".join(strings)

    except Exception as e:
        print(e)
        return "CHECK THIS."


