from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = "commented.txt"
header = "**Explanation of this xkcd**\n"
footer = '\n*---This explanation was extracted from [explainxkcd](http://www.explainxkcd.com)*'


def authenticate():
    print("Authenticating...\n")
    reddit = praw.Reddit("BookInfoBot", user_agent='web:bookinfobot v0.1 ')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find(id="description")
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

def run_explainbot(reddit):
    
    print("Getting 250 comments...\n")
    
    for comment in reddit.subreddit('test').comments(limit = 250):
        match = re.findall("[a-z]*[A-Z]*[0-9]*https://www.xkcd.com/[0-9]+", comment.body)
        if match:
            print("Link found in comment with comment ID: " + comment.id)
            xkcd_url = match[0]
            url_obj = urlparse(xkcd_url)
            xkcd_id = int((url_obj.path.strip("/")))
            myurl = 'http://www.explainxkcd.com/wiki/index.php/' + str(xkcd_id)
            
            file_obj_r = open(path,'r')
                        
            try:
                explanation = fetchdata(myurl)
            except:
                print('Exception!!! Possibly incorrect xkcd URL...\n')
                # Typical cause for this will be a URL for an xkcd that does not exist (Example: https://www.xkcd.com/772524318/)
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(header + explanation + footer)
                    
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
            
            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)

def main():
    reddit = authenticate()
    while True:
        run_explainbot(reddit)

if __name__ == '__main__':
    main()