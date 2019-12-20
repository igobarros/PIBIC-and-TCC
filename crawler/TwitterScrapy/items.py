# -*- coding: utf-8 -*-

from scrapy import Item, Field


class TwitterItem(Item):
    
    ID = Field()       # tweet id
    url = Field()      # tweet url
    datetime = Field() # post time
    text = Field()     # text content
    user_id = Field()  # user id
    usernameTweet = Field() # username of tweet

    number_retweet = Field() # number of retweet
    number_favorite = Field() # number of favorite
    number_reply = Field() # number of reply

    is_reply = Field() # boolean if the tweet is a reply or not
    is_retweet = Field() # boolean if the is just a retweet of another tweet