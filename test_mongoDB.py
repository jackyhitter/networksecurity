
import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
uri = os.getenv("MONGO_DB_URL")

if not uri:
    raise ValueError("MONGO_DB_URL is not set. Add it to the .env file.")

client = None
try:
    # Create a new client and send a ping to confirm the connection.
    client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
finally:
    if client is not None:
        client.close()
