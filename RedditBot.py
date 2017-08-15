from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = "commented.txt"
header = "**Description of Books** \n\n"
pages = "\n**Total Pages:** "
footer = '\n\n**---This description was extracted from [Goodreads](https://www.goodreads.com/) ---**'


def authenticate():
    print("Authenticating...\n")
    reddit = praw.Reddit("BookInfoBot", user_agent='web:bookinfobot v0.1 ')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    book_details = soup.find(id="description")
    book_details = book_details.span.next_sibling.next_sibling.contents[0]

    num_pages = soup(itemprop="numberOfPages")[0].get_text() #soup.find(id="details")
    #num_pages = num_pages.div.span.next_sibling.next_sibling.contents
    return (book_details, num_pages)

def run_bookbot(reddit):
    key = "!book"
    print("Getting 250 comments...\n")
    for comment in reddit.subreddit('test').comments(limit = 250):
        
        if key in comment.body:
            #print("Link found in comment with comment ID: " + comment.id)
            text = comment.body
            book_url = extract_bookURL(text, key)

            file_obj_r = open(path,'r')

            try:
                description = str(fetchdata(book_url)[0])
                num_pages = fetchdata(book_url)[1]
            except:
                print("Possibly Incorrect book name or color")
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(header + description + pages + str(num_pages) + footer)
                    
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
            
            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)

def extract_bookURL(text, key):

    print("Some text is", text)
    book_name = text[text.index(key)+ len(key)+1:]

    print("book name is", book_name)
    goodreads_search = 'https://www.goodreads.com/search?q=' + book_name
    print("URL is", goodreads_search)

    r = requests.get(goodreads_search)
    soup = BeautifulSoup(r.content, "html.parser")
    first_book_url = soup.find("a", class_="bookTitle")['href']
    book_url = "https://www.goodreads.com" + first_book_url

    return book_url
    
def main():
    reddit = authenticate()
    while True:
        run_bookbot(reddit)

if __name__ == '__main__':
    main()