from pymongo import MongoClient
from decouple import config
import dns

def get_connection(collection_name):
    client=MongoClient(config('MONGO_URL'))
    collection=client[config("MONGO_DB")][collection_name]
    # if collection.acknowledged:
    #     print("Mongo db not connected")
    #     return False
    return collection