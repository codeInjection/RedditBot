from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4


header = "**Explanation of this xkcd**\n"
footer = '\n*---This explanation was extracted from [explainxkcd](http://www.explainxkcd.com)*'


def authenticate():
    print("Authenticating...\n")
    reddit = praw.Reddit("explainbot", user_agent='web:xkcd-explain-bot:v0.1 ')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.name == 'h2':
                break
            if tag.name == 'h3':
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
    return data