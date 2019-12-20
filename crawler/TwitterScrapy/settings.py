# -*- coding: utf-8 -*-

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'TwitterScrapy'

BOT_NAME = 'TwitterScrapy' # settings for spiders

#LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['TwitterScrapy.spiders']
NEWSPIDER_MODULE = 'TwitterScrapy.spiders'

#DOWNLOAD_HANDLERS = {'s3': None,} # from http://stackoverflow.com/a/31233576/2297751, TODO

# Configure item pipelines
ITEM_PIPELINES = {
    #'TwitterScrapy.pipelines.SaveToMongoPipeline': 300,
}

# settings for database mongodb
MONGODB_SERVER_PORT = "mongodb://user:passoword@localhost:27017/admin" # URI
MONGODB_DB = "DBNAME"        # database name to save the crawled data
MONGODB_TWEET_COLLECTION = "COLECCTION_NAME" # collection name to save tweets

#DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'