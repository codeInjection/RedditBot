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