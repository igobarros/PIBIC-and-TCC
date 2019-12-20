import logging

import pandas as pd
from pymongo import MongoClient

from settings import CONFIG_PROD

logger = logging.getLogger(__name__)

class MongoDB:

	def __init__(self):
		self.__conn = MongoClient(CONFIG_PROD['MONGO_URI'])
		self.__db = self.__conn[CONFIG_PROD['MONGO_DBNAME']]
		self.__collection = self.__db[CONFIG_PROD['COLLECTION_NAME']]


	def dataset(self, is_excludedata=True):

		exclude_data = {

			"_id": False, "ID": False, "url": False, 
			"user_id": False, "usernameTweet": False, "datetime": False, 
			"is_ply": False, "is_retweet": False, "number_favorite": False, 
			"number_reply": False, "number_retweet": False, "is_reply": False
		}

		if is_excludedata:
			df = pd.DataFrame.from_records(data=self.__collection.find({}, projection=exclude_data))
			return df
		else:
			df = pd.DataFrame.from_records(data=self.__collection.find({}))
			return df


