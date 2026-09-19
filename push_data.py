import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()


import pandas as pd
import pymongo
from pymongo.server_api import ServerApi
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  

class NetworkDataExtractor:
    def __init__(self, database_name: str, collection_name: str):
        self.database_name = database_name
        self.collection_name = collection_name

    def csv_to_json_converter(self, csv_file_path: str) -> list:
        try:
            logging.info(f"Converting CSV file to JSON: {csv_file_path}")
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.to_json()).values())
            logging.info(f"CSV file converted to JSON successfully: {csv_file_path}")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_to_mongodb(self, records: list) -> int:
        try:
            if not MONGO_DB_URL:
                raise ValueError("MONGO_DB_URL is not set. Add it to the .env file.")
            if not records:
                return 0

            with pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca,
                server_api=ServerApi("1"),
                serverSelectionTimeoutMS=10_000,
            ) as mongo_client:
                mongo_client.admin.command("ping")
                collection = mongo_client[self.database_name][self.collection_name]
                collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

if __name__ == '__main__':
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "idontwannashowthis"
    COLLECTION = "NetworkData"
    networkobj = NetworkDataExtractor(DATABASE, COLLECTION)
    records = networkobj.csv_to_json_converter(csv_file_path=FILE_PATH)
    no_of_records = networkobj.insert_data_to_mongodb(records)
    print(no_of_records)
    
