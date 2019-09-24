#!/usr/bin/env/python
"""
GIF bot application.

Original author: Tahmid Efaz, tahmidefaz@gmail.com
Date: 2017/07/21
"""
import json
import requests
import time
import urllib.request

import tweepy


GIPHY_API_KEY = "" # TODO: obtain this key from https://developers.giphy.com/

# TODO: obtain the following keys from https://dev.twitter.com/
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""


def modifier(s):
    """
    Return hashtags based on the GIF names from GIPHY.
    """
    ms =''
    for i in range(len(s)):
        if(s[i] == '-'):
            ms += ' '
        else:
            ms += s[i]
    ls = ms.split()
    del ls[-1]
    ls[0] = "#" + ls[0]
    
    return (" #".join(ls))


def gif_download(gif_url):
    """
    Take the URL of an Image/GIF and download it.
    """
    gif_data = requests.get(gif_url).content
    
    with open('image.gif', 'wb') as handler:
        handler.write(gif_data)

        
def tweet(tweet_msg):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    message = tweet_msg + " #funny #gif #lol #humor" # TODO: Add desired tweet message here
    api.update_with_media('image.gif',status=message)


def gif_post(gif_url_list, msg):
    """
    Tweet GIFs and sleep for a specific time.
    """
    for i in range(len(gif_url_list)):
        try:
            gif_download(gif_url_list[i])
            m = modifier(msg[i])
            tweet(m)
        except:
            continue
        time.sleep(900) #TODO: Change this number to modify how often each tweet gets posted


def main():
    while True:
        giphy_url = "http://api.giphy.com/v1/gifs/trending?&api_key=" + GIPHY_API_KEY + "&limit=30"

        with urllib.request.urlopen(giphy_url) as response:
           html = response.read()

        h = html.decode("utf-8")
        gif_info = json.loads(h)
        gif_data = gif_info["data"]
        gif_urls = []
        slugs = []

        for i in range(len(gif_data)):
            gif = gif_data[i]['images']["downsized"]["url"]
            slug = gif_data[i]['slug']
            gif_urls.append(gif)
            slugs.append(slug)

        gif_post(gif_urls, slugs)
        gif_urls = []
        slugs = []
        
        
if __name__ == '__main__':
    main()
