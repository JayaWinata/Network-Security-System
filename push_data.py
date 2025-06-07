import os
import sys
import json
import certifi

import numpy as np
import pandas as pd
import pymongo

from src.exception.exception import NetworkSecurityException
from src.logging.logger import logger

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()

class NetworkDataExtract():
    def __init__(self, database, collection):
        try:
            self.database = database
            self.collection = collection
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.drop(columns=['index'], inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_db(self, records):
        try:
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(records)
            return(len(records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__=='__main__':
    FILE_PATH="dataset\Dataset Phising Website.csv"
    DATABASE="NetworkSecuritySystem"
    COLLECTION="NetworkData"
    networkobj=NetworkDataExtract(DATABASE, COLLECTION)
    records=networkobj.csv_to_json(file_path=FILE_PATH)
    # print(records)
    no_of_records=networkobj.insert_data_to_db(records)
    logger.info(f'{no_of_records} records inserted to MongoDB successfully!')
