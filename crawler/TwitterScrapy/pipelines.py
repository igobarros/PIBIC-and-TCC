# -*- coding: utf-8 -*-

import pymongo
import logging

from scrapy.utils.project import get_project_settings

settings = get_project_settings()

logger = logging.getLogger(__name__)

class SaveToMongoPipeline(object):

    '''pipeline that save data to mongodb'''
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.tweetCollection = db[settings['MONGODB_TWEET_COLLECTION']]
        self.tweetCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)


    def process_item(self, item, spider):
        self.tweetCollection.insert_one(dict(item))
        logger.debug("Add tweet:%s" %item['url'])


